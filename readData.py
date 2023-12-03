import csv
from collections import defaultdict
import numpy as np


def csv_to_list(file_name):
    d = []
    with open(file_name, newline='') as csv_file:
        reader = csv.reader(csv_file)
        for line in reader:
            d.append({'user_id': line[0], 'recipe_id': line[1], 'date': line[2], 'rating': line[3], 'u': line[4], 'i': line[5]})
    return d[1:]

def MSE(y, ypred):
    return sum(x**2 for x in (y - ypred)) / len(y)

data_train = csv_to_list('interactions_train.csv')
data_valid = csv_to_list('interactions_validation.csv')
data_test = csv_to_list('interactions_test.csv')

def calculateBaselines() : 

    # Baseline 1: predict global average rating for any review

    sum([float(d['rating']) for d in data_train]) / len(data_train)

    global_average_rating = round(sum([float(d['rating']) for d in data_train]) / len(data_train))
    global_average_rating

    test_Y = [float(d['rating']) for d in data_test]
    predict_Y = [5 for _ in data_test]

    correct = sum(int(test_Y[i] == predict_Y[i]) for i in range(len(test_Y))) / len(test_Y)
    print("BL1 Num Correct: ", correct)

    mse = MSE(test_Y, np.array(predict_Y))

    print("BL1 MSE: " , mse)

    # Baseline 2: predict average rating that a user gives
    user_ratings = defaultdict(list)

    for d in data_train:
        user_ratings[d['user_id']].append(float(d['rating']))

    predict_Y = [round(sum(user_ratings[d['user_id']]) / len(user_ratings[d['user_id']])) if len(user_ratings[d['user_id']]) else 5 for d in data_test]
    # sum([len(recipe_ratings[d['recipe_id']]) for d in data_test])
    correct = sum(int(test_Y[i] == predict_Y[i]) for i in range(len(test_Y))) / len(test_Y)
    print("BL2 Num correct: " , correct) 
    
    mse2 = MSE(test_Y, np.array(predict_Y))
    print("BL2 MSE: " , mse2) 


#All recipes contains all the recipes from PP_recipes.csv as a dictionary that
#takes in the recipeID as integers (not the tokenized ones and has the following
#fields available: techniques, calories, ingredients
#ie to access the ingredients for recipe # 424415 you'd use
#allRecipes[424415]['ingredients']
recipes = defaultdict(dict)


with open("PP_recipes.csv") as allRecipes :
    reader = csv.reader(allRecipes)
    for d in reader:
        if d[0] == "id" :
            continue 
        recipeID = int(d[0])
        
        #techniques = d[-3]
        #calories = d[-2]
        #ingredients = d[-1]
        recipes[recipeID] = {
            "tokenizedID" : int(d[1]) ,
            "name_tokens" : d[2], 
            "ingredients_tokens" : d[3],
            "steps_tokens" : d[4],
            "techniques" : d[5] ,
            "calorie_level" : d[6] ,
            "ingredients" : d[7]
            }
            
        


if (len(recipes) == 178265) :
    print("All recipes loaded successfully.")
    #Kaggle says its 178265, profs site says 231,637


#Read in PP_users.csv and all its fields

users = defaultdict(dict)


with open("PP_users.csv") as allUsers :
    reader = csv.reader(allUsers)
    for d in reader:
        if d[0] == "u" :
            continue

        tokenizedID = int(d[0])

        users[tokenizedID] = {
            "techniques" : d[1] ,
            "items" : d[2] ,
            "numItems" : d[3] ,
            "ratings" : d[4] ,
            "n_ratings" : d[5]
            }
            
        
       
            


