from flask import Flask, jsonify, request 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS




app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})


 



# MySQL Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://navin:navin@localhost/stress_assessment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkeythatissufficientlylongandsecure'  # Change this to a real secret key

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    # Relationship to UserResponse
    responses = db.relationship('UserResponse', backref='user', lazy=True)

# Define the UserResponse model
class UserResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answer1 = db.Column(db.Integer, nullable=False)
    answer2 = db.Column(db.Integer, nullable=False)
    answer3 = db.Column(db.Integer, nullable=False)
    answer4 = db.Column(db.Integer, nullable=False)
    answer5 = db.Column(db.Integer, nullable=False)
    stress_level = db.Column(db.String(20), nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=False)


# Define the Questions (static for now)
questions = [
    "On a scale of 1 to 5, how overwhelmed do you feel with your daily tasks? (1 = not at all, 5 = extremely)",
    "How often do you find it difficult to relax or unwind? (1 = never, 5 = always)",
    "How frequently do you experience headaches or muscle tension? (1 = never, 5 = very often)",
    "Do you feel anxious or worried without a clear reason? (1 = never, 5 = always)",
    "How often do you have trouble sleeping or feel fatigued during the day? (1 = never, 5 = always)"
]

# Function to evaluate stress level based on answers
def evaluate_stress(answers):
    total_score = sum(answers)
    max_score = len(answers) * 5

    if total_score <= max_score * 0.3:
        return "low stress"
    elif total_score <= max_score * 0.6:
        return "moderate stress"
    else:
        return "high stress"

# API endpoint to register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    phone = data['phone']

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists!'}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create a new user
    new_user = User(username=username, email=email, password=hashed_password, phone=phone)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201

# API endpoint to login a user and return JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login successful!', 'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid email or password!'}), 401

# API endpoint to fetch questions
@app.route('/questions', methods=['GET'])
def get_questions():
    return jsonify({"questions": questions})

# API endpoint to submit answers and store them in the database
@app.route('/stress-evaluation', methods=['POST'])
@jwt_required()
def evaluate_stress_level():
    data = request.get_json()
    user_id = get_jwt_identity()

    # Ensure valid data is provided
    if not data or "answers" not in data or not isinstance(data["answers"], list):
        return jsonify({"error": "Invalid input data. Please provide a list of answers."}), 400

    answers = data["answers"]

    # Check if all answers are between 1 and 5
    if not all(isinstance(a, int) and 1 <= a <= 5 for a in answers):
        return jsonify({"error": "All answers must be integers between 1 and 5."}), 400

    if len(answers) != len(questions):
        return jsonify({"error": f"Please provide {len(questions)} answers."}), 400

    # Evaluate the stress level
    stress_level = evaluate_stress(answers)

    # Store the answers and stress level in the database
    user_response = UserResponse(
        user_id=user_id,
        answer1=answers[0],
        answer2=answers[1],
        answer3=answers[2],
        answer4=answers[3],
        answer5=answers[4],
        stress_level=stress_level
    )
    db.session.add(user_response)
    db.session.commit()

    return jsonify({"stress_level": stress_level})

 
# API endpoint to get all responses of the logged-in user (for testing purposes)
@app.route('/my-responses', methods=['GET'])
@jwt_required()
def get_my_responses():
    user_id = get_jwt_identity()

    # Fetch responses of the logged-in user
    responses = UserResponse.query.filter_by(user_id=user_id).all()
    response_list = [
        {
            "id": response.id,
            "answers": [response.answer1, response.answer2, response.answer3, response.answer4, response.answer5],
            "stress_level": response.stress_level,
            "created_at": response.created_at
        }
        for response in responses
    ]

    return jsonify(response_list), 200




@app.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()  # Get user ID from JWT token
    user = User.query.get(user_id)  # Fetch user from database

    if user:
        user_info = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone
        }
        return jsonify(user_info), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/contacts', methods=['POST'])
@jwt_required()
def add_contact():
    user_id = get_jwt_identity()
    data = request.get_json()
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')

    if not email or not phone or not address:
        return jsonify({'error': 'Missing required fields.'}), 400

    # Create a new contact
    new_contact = Contact(user_id=user_id, email=email, phone=phone, address=address)
    db.session.add(new_contact)
    db.session.commit()

    return jsonify({'message': 'Contact added successfully!'}), 201



if __name__ == '__main__':
    app.run(debug=True)
