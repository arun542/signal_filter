import os, datetime, time

#### check for any floating point number in string
def check_for_numbers(words):
	for word in words:
		try:
			number = float(word)
			return number
		except:
			continue
	return None

#### checks for any date, time or datetime obj in string
def check_for_date(words):
	date = None 
	time = None
	datetime_string = None
	date_type = None
	for word in words:
		try:
			date = datetime.datetime.strptime(word, "%Y-%M-%d")
			date = word
		except:
			date = None
		try:
			time = datetime.datetime.strptime(word, "%H:%m:%S")
			time = word
		except:
			time = None
	if date:
		if time:
			datetime_string = date + " " + time
			date_type = "datetime"
		else:
			datetime_string = date + " 00:00:00"
	else:
		if time:
			datetime_string = time
			date_type = "time"

	return datetime_string, date_type

######## Rules Class ###########
class Rules(object):
	def __init__(self, path=None):
		self.defualt_path = "rules.txt"
		self.rules_text = []
		self.rules_dict = {}
		self.parsed_rules = []
		self.rule_file_path = None
		self.create_rules_dict(path)

	def update_rule_path(self,path):
		try:
			file_obj = open(path,"r")
			self.rule_file_path = path
			self.rules_text = []
			self.rules_dict = {}
			self.parsed_rules = []

			all_rule_strings = file_obj.read().splitlines()
			all_rules = {}
			for rule_string in all_rule_strings:
				try:
					parsed_rule = self.parse_rule_string(rule_string)
					if parsed_rule is not None:
						if parsed_rule["signal"] in all_rules.keys():
							if parsed_rule["type"] in all_rules[parsed_rule["signal"]].keys():
								all_rules[parsed_rule["signal"]][parsed_rule["type"]] = all_rules[parsed_rule["signal"]][parsed_rule["type"]] + [{"value":parsed_rule["value"],"comparison":parsed_rule["comparison"]}]
							else:
								all_rules[parsed_rule["signal"]][parsed_rule["type"]] = [{"value":parsed_rule["value"],"comparison":parsed_rule["comparison"]}]
						else:
							all_rules[parsed_rule["signal"]] = {}
							all_rules[parsed_rule["signal"]][parsed_rule["type"]] = [{"value":parsed_rule["value"],"comparison":parsed_rule["comparison"]}]
					
						self.rules_text.append(rule_string)
						self.parsed_rules.append(parsed_rule)

				except:
					print "error in parsing rule "+rule_string

			self.rules_dict = all_rules
			print "Rules file updated"
		except:
			print path, " file doesnot exist"


	def create_rules_dict(self, path=None):
		try:
			if not path:
				file_obj = open(self.defualt_path,"r")
				self.rule_file_path = self.defualt_path
			else:
				file_obj = open(path,"r")
				self.rule_file_path = path

			all_rule_strings = file_obj.read().splitlines()
			all_rules = {}
			for rule_string in all_rule_strings:
				try:
					parsed_rule = self.parse_rule_string(rule_string)
					if parsed_rule is not None:
						if parsed_rule["signal"] in all_rules.keys():
							if parsed_rule["type"] in all_rules[parsed_rule["signal"]].keys():
								all_rules[parsed_rule["signal"]][parsed_rule["type"]] = all_rules[parsed_rule["signal"]][parsed_rule["type"]] + [{"value":parsed_rule["value"],"comparison":parsed_rule["comparison"]}]
							else:
								all_rules[parsed_rule["signal"]][parsed_rule["type"]] = [{"value":parsed_rule["value"],"comparison":parsed_rule["comparison"]}]
						else:
							all_rules[parsed_rule["signal"]] = {}
							all_rules[parsed_rule["signal"]][parsed_rule["type"]] = [{"value":parsed_rule["value"],"comparison":parsed_rule["comparison"]}]
					
						self.rules_text.append(rule_string)
						self.parsed_rules.append(parsed_rule)

				except:
					print "error in parsing rule "+rule_string

			self.rules_dict = all_rules
		except:
			print "no rules found"

	def print_current_rules(self):
		print "all rules:"
		for i,rule in enumerate(self.rules_text):
			print "id : ",i, "  rule : ",rule

	def add_new_rule(self, new_rule):
		parsed_rule = self.parse_rule_string(new_rule)
		all_rules = self.rules_dict
		if parsed_rule is not None:
			if parsed_rule["signal"] in all_rules.keys():
				if parsed_rule["type"] in all_rules[parsed_rule["signal"]].keys():
					all_rules[parsed_rule["signal"]][parsed_rule["type"]] = all_rules[parsed_rule["signal"]][parsed_rule["type"]] + [{"value":parsed_rule["value"],"comparison":parsed_rule["comparison"]}]
				else:
					all_rules[parsed_rule["signal"]][parsed_rule["type"]] = [{"value":parsed_rule["value"],"comparison":parsed_rule["comparison"]}]
			else:
				all_rules[parsed_rule["signal"]] = {}
				all_rules[parsed_rule["signal"]][parsed_rule["type"]] = [{"value":parsed_rule["value"],"comparison":parsed_rule["comparison"]}]
		
			self.rules_text.append(new_rule)
			self.parsed_rules.append(parsed_rule)
		# print all_rules
		self.rules_dict = all_rules
		with open(self.rule_file_path, "w") as f:
			for rule in self.rules_text:
				f.write(rule+"\n")

	def remove_rule(self, rule_id):
		try:
			rule_id = int(rule_id)
			if rule_id < len(self.rules_text):
				parsed_rule = self.parsed_rules[rule_id]
				all_rules = self.rules_dict
				check_rules = all_rules[parsed_rule["signal"]][parsed_rule["type"]]
				new_rules = []
				for rule in check_rules:
					if rule["value"] == parsed_rule["value"] and rule["comparison"] == parsed_rule["comparison"]:
						pass
					else:
						new_rules.append(rule)
				if len(new_rules) ==0:
					all_rules[parsed_rule["signal"]].pop(parsed_rule["type"], None)
					if len(all_rules[parsed_rule["signal"]].keys()) == 0:
						all_rules.pop(parsed_rule["signal"], None)
				else:
					all_rules[parsed_rule["signal"]][parsed_rule["type"]] = new_rules
				self.rules_dict = all_rules

				del self.parsed_rules[rule_id]
				del self.rules_text[rule_id]

				with open(self.rule_file_path, "w") as f:
					for rule in self.rules_text:
						f.write(rule+"\n")
				print "Rule successfuly deleted"

			else:
				print "Not valid rule ID"
		except:
			print "Not valid rule ID"

	######### parses rule to dict form from string ######
	def parse_rule_string(self,rule_string, contradiction_flag = True):
		split_string = rule_string.split(" ")
		signal = split_string[0]
		value, signal_type, comparison = self.get_value_type(split_string)

		if value and signal_type and comparison:
			new_rule = {"value":value,"type":signal_type,"comparison":comparison,"signal":signal}
			duplicacy_check = self.check_for_duplicacy(new_rule)
			if duplicacy_check:
				print "Duplicacy : The rule "+ rule_string + " already exists"
			else:
				if contradiction_flag:
					contadicting_rule, contradiction_check = self.check_for_contradiction(new_rule)
					if contradiction_check:
						print "The rule "+ rule_string + " contadicts with " + contadicting_rule
					else:
						return new_rule
				else:
					return new_rule
		else:
			print "Could not parse rule "+rule_string
			return None

	########### GIven string of rules returns the value, comparison string and type of rule #########
	def get_value_type(self,words):
		value = None
		rule_type = None
		comparison = None
		if "LOW" in words:
			rule_type = "String"
			value = "LOW"
			if "not" in words or "never" in words:
				comparison = "!="
			else:
				comparison = "=="

		elif "MEDIUM" in words:
			rule_type = "String"
			value = "MEDIUM"
			if "not" in words or "never" in words:
				comparison = "!="
			else:
				comparison = "=="

		elif "HIGH" in words:
			rule_type = "String"
			value = "HIGH"
			if "not" in words or "never" in words:
				comparison = "!="
			else:
				comparison = "=="

		else:
			value = check_for_numbers(words)
			if value:
				rule_type = "Integer"
				value = value
				if "not" in words or "never" in words:
					if "equal" in words:
						comparison = "!="

					if "greater" in words or "larger" in words or "bigger" in words or "rise" in words or "increase" in words or "above" in words:
						comparison = "<="

					if "smaller" in words or "larger" in words or "bellow" in words or "fall" in words or "decrease" in words:
						comparison = ">="

				else:
					if "equal" in words:
						comparison = "=="

					if "greater" in words or "larger" in words or "bigger" in words or "rise" in words or "increase" in words or "above" in words:
						comparison = ">"

					if "smaller" in words or "larger" in words or "bellow" in words or "fall" in words or "decrease" in words:
						comparison = "<"
			else:
				date, date_type = check_for_date(words)
				if date:
					rule_type = date_type
					value = date
					if "not" in words or "never" in words:
						if "equal" in words:
							value = value.split(" ")[0]
							rule_type = "date"
							comparison = "!="

						if "on" in words:
							comparison = "not in"
							value = value.split(" ")[0]
							rule_type = "date"

						if "greater" in words or "after" in words  or "later" in words:
							comparison = "<="

						if "smaller" in words or "before" in words or "till" in words or "untill" in words:
							comparison = ">="

					else:
						if "equal" in words:
							comparison = "=="
							
						if "on" in words:
							comparison = "in"
							value = value.split(" ")[0]
							rule_type = "date"

						if "greater" in words or "after" in words  or "later" in words:
							comparison = ">"

						if "smaller" in words or "before" in words or "till" in words or "untill" in words:
							comparison = "<"
				else:
					if "today" in words:
						rule_type = "dateobj"
						value = "today"

					if "tomorrow" in words:
						rule_type = "dateobj"
						value = "tomorrow"
						

					if "yesterday" in words:
						rule_type = "dateobj"
						value = "yesterday"

					if "future" in words:
						rule_type = "dateobj"
						value = "future"

					if "past" in words:
						rule_type = "dateobj"
						value = "future"

					if "not" in words or "never" in words or "past" in words:
						if "after" in words:
							comparison = "<="
							

						elif "before" in words or "till" in words or "untill" in words:
							comparison = ">="
							print words
						else:
							comparison = "not in"
					else:
						if "after" in words:
							comparison = ">"

						elif "before" in words or "till" in words or "untill" in words:
							comparison = "<"
						else:
							comparison = "in"

		return value, rule_type, comparison

	def check_for_duplicacy(self,rule):
		all_rules = self.rules_dict
		if rule["signal"] in all_rules.keys():
			if rule["type"] in all_rules[rule["signal"]].keys():
				existing_rules = all_rules[rule["signal"]][rule["type"]]
				for check_rule in existing_rules:
					if check_rule["comparison"] == rule["comparison"] and check_rule["value"] == rule["value"]:
						return True
		return False

	def check_for_contradiction(self,check_rule):
		rules = self.rules_dict
		if check_rule["signal"] not in rules.keys():
			return None, False
		else:
			signal_rules = rules[check_rule["signal"]]
			check_string = ""
			if check_rule["type"] == "String" or check_rule["type"] == "Integer":
				if check_rule["type"] in signal_rules.keys():
					applied_rules = signal_rules[check_rule["type"]]
					if len(applied_rules)>1:
						for rule in applied_rules:
							if check_rule["type"] == "Integer":
								check_string  = check_string +str(check_rule["value"]) + " " + rule["comparison"] +" "+ str(rule["value"]) +" and "
							else:
								check_string  = check_string + "'"+str(check_rule["value"]) + "' " + rule["comparison"] +" '"+ rule["value"] +"' and "
						check_string = check_string + " True"
					else:
						if check_rule["type"] == "Integer":
							check_string = str(check_rule["value"]) + " " + applied_rules[0]["comparison"] +" "+ str(applied_rules[0]["value"])
						else:
							check_string = "'"+str(check_rule["value"]) + "' " + applied_rules[0]["comparison"] +" '"+ str(applied_rules[0]["value"])+"'"

					pass_fail  = eval(check_string)
					return check_string, not pass_fail
			else:
				if "datetime" in signal_rules.keys():
					applied_rules = signal_rules["datetime"]

					for rule in applied_rules:
						check_string  = check_string+ "'"+str(check_rule["value"]) + "' " + rule["comparison"] +" '"+ rule["value"] +"' and "

				if "date" in signal_rules.keys():
					applied_rules = signal_rules[check_rule["date"]]
					
					for rule in applied_rules:
						check_string = check_string+ "'"+str(check_rule["value"]).split(" ")[0] + "' " + rule["comparison"] +" '"+ rule["value"] +"' and "

				if "dateobj" in signal_rules.keys():
					applied_rules = signal_rules["dateobj"]
					for rule in applied_rules:
						date = None
						if rule["value"] == "today":
							date = datetime.date.today()
							date = date.strftime("%Y-%m-%d")

						if rule["value"] == "tomorrow":
							date = datetime.date.today()
							date = date + datetime.timedelta(days=1)
							date = date.strftime("%Y-%m-%d")

						if rule["value"] == "yesterday":
							date = datetime.date.today()
							date = date - datetime.timedelta(days=1)
							date = date.strftime("%Y-%m-%d")

						if date and (rule["comparison"] != "in" or rule["comparison"] != "not in"):
							date = date + " 00:00:00"
							signal_value = check_rule["value"]
						else:
							signal_value = str(check_rule["value"]).split(" ")[0]

						if rule["value"] == "future":
							date = datetime.date.today()
							date = time.strftime("%Y-%m-%d %H-%M-%S")
							signal_value = check_rule["value"]

						check_string = check_string + "'"+signal_value + "' " + rule["comparison"] +" '"+ date +"' and "

				if "time" in signal_rules.keys() and len(signal_rules[check_rule["time"]])>0:
					applied_rules = signal_rules["time"]
					
					for rule in applied_rules:
						check_string = check_string+ "'"+str(check_rule["value"]).split(" ")[1] + "' " + rule["comparison"] +" '"+ rule["value"] +"' and "

				check_string = check_string + " True"
				pass_fail  = eval(check_string)
				return check_string, not pass_fail
			return None, False

#check for contradiction and duplicacy

if __name__ == "__main__":
	new_Rules = Rules()



