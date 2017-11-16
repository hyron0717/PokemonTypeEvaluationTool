import requests
import sys

## translate the pokemon's id to pokemon's name
## input: pokemon's name or id
## output: pokemon's name
def getName(id):
	url = "http://pokeapi.co/api/v2/pokemon/" + id
	response = requests.get(url)
	data = response.json()
	name = data["name"]
	return name

## find the type given the name or id
## input: pokemon's name or id
## output: the list of type the pokemon have
def getType(name):
	url = "http://pokeapi.co/api/v2/pokemon/" + name
	response = requests.get(url)
	data = response.json()

	types = data["types"]
	types_list = []

	for i in range(0,len(types)):
		temp = types[i]["type"]["name"]
		types_list.append(temp)

	return types_list

## find which pokemon can be beaten by this pokemon
## input: pokemon's type
## output: the list of all the pokemons have less type advantage
def getWinType(name):
	url = "http://pokeapi.co/api/v2/type/" + name
	response = requests.get(url)
	data = response.json()

	win_words = ["half_damage_from", "no_damage_from", "double_damage_to"]
	win_types_list = []

	for j in win_words:
		win_types = data["damage_relations"][j]

		for i in range(0,len(win_types)):
			temp = win_types[i]["name"]
			if temp not in win_types_list:
				win_types_list.append(temp)

	return win_types_list

## find which pokemon cannot be beaten by this pokemon
## input: pokemon's type
## output: the list of all the pokemons have better type advantage
def getLoseType(name):
	url = "http://pokeapi.co/api/v2/type/" + name
	response = requests.get(url)
	data = response.json()

	lose_words = ["half_damage_to", "double_damage_from", "no_damage_to"]
	lose_types_list = []

	for j in lose_words:
		lose_types = data["damage_relations"][j]

		for i in range(0,len(lose_types)):
			temp = lose_types[i]["name"]
			if temp not in lose_types_list:
				lose_types_list.append(temp)

	return lose_types_list

## sum all 6 stat of the pokemon
## input: pokemon's name or id
## output: the total stat
def getTotalStat(name):
	url = "http://pokeapi.co/api/v2/pokemon/" + name
	response = requests.get(url)
	data = response.json()

	pokemon_stats = data["stats"]
	total_stat = 0
	for i in range(0,len(pokemon_stats)):
		temp = pokemon_stats[i]["base_stat"]
		total_stat = total_stat + temp

	return total_stat

## determine the winner in comparison
## input: list of input pokemon's name, their type, which pokemon they can beat, which pokemon they will lose
## output: the winner's name
def check(name_list, type_list, total_win_list, total_lose_list):
	for i in range(0, len(name_list)):
		count = 0
		for j in range(0, len(name_list)):
			if i == j:
				count = count + 1
				continue

			temp_win = total_win_list[j]
			temp_lose = total_lose_list[j]

			if len(type_list[i]) == 1:
				if type_list[i][0] not in temp_win and type_list[i][0] in temp_lose:
					count = count + 1
			else:
				if (type_list[i][0] not in temp_win and type_list[i][1] not in temp_win) and (type_list[i][0] in temp_lose or type_list[i][1] in temp_lose):
					count = count + 1

		if count == len(name_list):
			return name_list[i]

	total_stat_list = []

	for i in range(0, len(name_list)):
		temp_stat = getTotalStat(name_list[i])
		total_stat_list.append(temp_stat)

	max_stat = max(total_stat_list)
	for i in range(0, len(name_list)):
		if max_stat == total_stat_list[i]:
			return name_list[i]


## main function
def __main__():
	num_args = len(sys.argv) - 1
	name_list = []
	type_list = []

	count = 0
	total_win_list = []
	total_lose_list = []

	if num_args < 2:
		print("need two pokemons to compare")
		return
	else:
		for i in range(0, num_args):
			pokemon = sys.argv[i+1].lower()
			type_list.append(getType(pokemon))
			name_list.append(getName(pokemon))

			win_list = getWinType(type_list[i][0])
			lose_list = getLoseType(type_list[i][0])

			if len(type_list[i])>1:
				temp = getWinType(type_list[i][1])
				for j in range(0,len(temp)):
					if temp[j] not in win_list:
						win_list.append(temp[j])

				temp = getLoseType(type_list[i][1])
				for j in range(0,len(temp)):
					if temp[j] not in lose_list:
						lose_list.append(temp[j])

			total_win_list.append(win_list)
			total_lose_list.append(lose_list)

	winner = check(name_list, type_list, total_win_list, total_lose_list)
	print(winner)

__main__()