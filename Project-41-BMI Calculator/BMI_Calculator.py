while True:
    print('--- Welcome!! Calculate your BMI ---')
    print('Choose the measurement system:')
    print('1. Metric (kg, cm)')
    print('2. Imperial (lbs, inch)')
    print('3. Exit')

    choice = input('Enter 1, 2 or 3: ')

    if choice == '3':
        print("Thank you for using the BMI calculator! Goodbye 👋")
        break

    if choice == '1':
        height = float(input('Enter your height in centimeters: '))
        weight = float(input('Enter your weight in kilograms: '))
        height = height / 100  # convert cm to meters

    elif choice == '2':
        height = float(input('Enter your height in inches: '))
        weight = float(input('Enter your weight in pounds: '))
        height = height * 0.0254  # convert inches to meters
        weight = weight * 0.4536  # convert pounds to kg

    else:
        print("❌ Invalid choice, please enter 1, 2, or 3.")
        continue

    if height <= 0 or weight <= 0:
        print("❌ Please enter valid height and weight.")
        continue

    bmi = weight / (height * height)
    print('📊 Your Body Mass Index is:', round(bmi, 2))

    if bmi <= 16:
        print('⚠️ Your weight is too low.')
    elif bmi <= 18.5:
        print('⚠️ Your weight is less than normal.')
    elif bmi <= 25:
        print('✅ Your weight is perfect (healthy range).')
    elif bmi <= 30:
        print('⚠️ Your weight is high, please exercise.')
    else:
        print('🚨 You are severely overweight.')

    print("-" * 40)  # separator line
    input('Press Enter to continue...')
