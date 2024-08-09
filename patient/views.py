from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from .models import DiabetesData

def home(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def hospital(request):
    return render(request, "hospital.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return render(request, 'data.html')
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already exist')
                return render(request, 'register.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already exist')
                return render(request, 'register.html')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                print('user created')
                return redirect('login')

        else:
            messages.info(request, 'Invalid Credentials')
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')

def predict(request):
    if request.method == 'POST':
        pregnancies = request.POST['pregnancies']
        glucose = request.POST['glucose']
        bloodpressure = request.POST['bloodpressure']
        skinthickness = request.POST['skinthickness']
        insulin = request.POST['insulin']
        bmi = request.POST['bmi']
        diabetespedigreefunction = request.POST['diabetespedigreefunction']
        age = request.POST['age']

        # Load and prepare the data
        df = pd.read_csv(r"static/dataset/diabetes (1).csv")
        df.dropna(inplace=True)
        X_train, X_test, y_train, y_test = train_test_split(
            df[['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']],
            df['Outcome'],
            test_size=0.2,
            random_state=42
        )

        # Train RandomForestClassifier
        rf = RandomForestClassifier()
        rf.fit(X_train, y_train)

        # Train DecisionTreeClassifier
        dt = DecisionTreeClassifier()
        dt.fit(X_train, y_train)

        # Create a DataFrame for input data
        input_data = pd.DataFrame(
            [[pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, diabetespedigreefunction, age]],
            columns=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
        )

        # Predict using both classifiers
        rf_prediction = rf.predict(input_data)[0]
        dt_prediction = dt.predict(input_data)[0]

        # Combine predictions
        combined_prediction = 1 if (rf_prediction + dt_prediction) >= 1 else 0

        # Calculate accuracies
        rf_accuracy = accuracy_score(y_test, rf.predict(X_test)) * 100
        dt_accuracy = accuracy_score(y_test, dt.predict(X_test)) * 100

        # Save the data
        Diabetes = DiabetesData.objects.create(
            Pregnancies=pregnancies, Glucose=glucose, BloodPressure=bloodpressure,
            SkinThickness=skinthickness, Insulin=insulin, BMI=bmi,
            DiabetesPedigreeFunction=diabetespedigreefunction, Age=age
        )
        Diabetes.save()

        return render(request, 'predict.html', {
            "rf_prediction": rf_prediction,
            "rf_accuracy": rf_accuracy,
            "dt_prediction": dt_prediction,
            "dt_accuracy": dt_accuracy,
            "combined_prediction": combined_prediction,
            'pregnancies': pregnancies,
            'glucose': glucose,
            'bloodpressure': bloodpressure,
            'skinthickness': skinthickness,
            'insulin': insulin,
            'bmi': bmi,
            'diabetespedigreefunction': diabetespedigreefunction,
            'age': age
        })

    else:
        return render(request, 'predict.html')
