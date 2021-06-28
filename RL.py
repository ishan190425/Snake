# Reward Eat Food +10
# Lose Game -10
# Else 0

# Possible Actions
# Up [1,0,0,0]
# Right [0,1,0,0]
# Left [0,0,1,0]
# Down [0,0,0,0]


# Current State (12 Values) (Inputs)
# [Danger Up, Left, Right, Down
# Direction Left, Right, Up, Down, (which way its oriented)
# Food Left, Right, Up, Down]

#Nural Network (Only One Hidden Level)
# 12 Input
# TBD Hidden
# 4 Outputs

#Deep Q Learning
#Q Value (Quailty of Action)
# 1) Init Q Value (= init model)
# 2) model.predict(state)) (or randome move) (Exploration vs Exploitation)
# 3) Perform Action
# 4) Measure Reward
# 5) Update Q Value( + train Model) Loss Function -> MSE
# (Repeat 2-5)