import random
print(random.randint(-10, +10))
coeff = {'tv': 1, 'sv': 1, 'cv': 1}
coeff['tv'] += random.randint(-10, +10)
coeff['cv'] += random.randint(-10, +10)
coeff['sv'] += random.randint(-10, +10)
print(coeff)