from rule_engine_parser import Rules
import os, datetime, json, time

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--rules", help="Pass a rule file. The file will get modified if you add or remove rules")
args = parser.parse_args()

## Fuction to run rules on array of singals
def run_test_on_signals(file_path, rules):
	try:
		json_data = json.load(open(file_path))
		print "Following signals didnot pass the corresponding criteria"
		time_start = datetime.datetime.now()
		for signal_data in json_data:
			##### check for any rules related to signal
			if signal_data["signal"] not in rules.keys():
				pass
			else:
				signal_rules = rules[signal_data["signal"]]
				check_string = ""
				#### check for type of rule
				if signal_data["value_type"] == "Datetime":

					if "datetime" in signal_rules.keys():
						applied_rules = signal_rules["datetime"]

						for rule in applied_rules:
							check_string  = check_string+ "'"+str(signal_data["value"]) + "' " + rule["comparison"] +" '"+ rule["value"] +"' and "

					if "date" in signal_rules.keys():
						applied_rules = signal_rules[signal_data["date"]]
						
						for rule in applied_rules:
							check_string = check_string+ "'"+str(signal_data["value"]).split(" ")[0] + "' " + rule["comparison"] +" '"+ rule["value"] +"' and "

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
								signal_value = signal_data["value"]
							else:
								signal_value = str(signal_data["value"]).split(" ")[0]

							if rule["value"] == "future":
								date = datetime.date.today()
								date = time.strftime("%Y-%m-%d %H-%M-%S")
								signal_value = signal_data["value"]

							check_string = check_string + "'"+signal_value + "' " + rule["comparison"] +" '"+ date +"' and "

					if "time" in signal_rules.keys() and len(signal_rules[signal_data["time"]])>0:
						applied_rules = signal_rules["time"]
						
						for rule in applied_rules:
							check_string = check_string+ "'"+str(signal_data["value"]).split(" ")[1] + "' " + rule["comparison"] +" '"+ rule["value"] +"' and "

					check_string = check_string + " True"
					pass_fail  = eval(check_string)
					if not pass_fail:
						print signal_data, applied_rules
					
				else:
					if signal_data["value_type"] in signal_rules.keys():
						applied_rules = signal_rules[signal_data["value_type"]]
						if len(applied_rules)>1:
							for rule in applied_rules:
								if signal_data["value_type"] == "Integer":
									check_string  = check_string +str(signal_data["value"]) + " " + rule["comparison"] +" "+ str(rule["value"]) +" and "
								else:
									check_string  = check_string + "'"+str(signal_data["value"]) + "' " + rule["comparison"] +" '"+ rule["value"] +"' and "
							check_string = check_string + " True"
						else:
							if signal_data["value_type"] == "Integer":
								check_string = str(signal_data["value"]) + " " + applied_rules[0]["comparison"] +" "+ str(applied_rules[0]["value"])
							else:
								check_string = "'"+str(signal_data["value"]) + "' " + applied_rules[0]["comparison"] +" '"+ str(applied_rules[0]["value"])+"'"

						pass_fail  = eval(check_string)
						if not pass_fail:
							print signal_data, applied_rules
		time_end = datetime.datetime.now()
		time_taken = time_end - time_start
		print "\ntime taken :", time_taken.total_seconds()
	except:
		print "Either file doesnot exist or Format is incorrect"

if __name__ == "__main__":
	if args.rules:
		rules = Rules(args.rules)
	else:
		rules = Rules()
	while True:
		task_choice = raw_input("\nENTER 1 to test on signals \nENTER 2 to change rules \nENTER 3 to quit\n")
		if task_choice == "1":

			while True:
				test_signal = raw_input("\nENTER 1 to test on default signals file \nENTER full file path to test on your own signal file\nENTER 3 to go back\n")
				if test_signal == "1":
					run_test_on_signals("raw_data.json", rules.rules_dict)
				elif test_signal == "3":
					break
				else:
					run_test_on_signals(test_signal, rules.rules_dict)

		elif task_choice == "2":
			while True:
				
				edit_rules_choice = raw_input("\nENTER 1 to print current Rules\nENTER 2 add new rule\nENTER 3 remove a rule\nENTER 4 to update rules file path \nENTER 5 to go back\n")
				
				if edit_rules_choice == "1":
					rules.print_current_rules()
				
				elif edit_rules_choice == "2":
					print "\nENTER new rule. Here are some tips to wrtite a RULE"
					print "\nYou should use LOW MEDIUM and HIGH\nFor integer comparison use greater, larger, bigger, rise, increase, above, smaller, larger, bellow, fall, decrease\nYou can use today, tomorrow, yesterday, future, past for time reference or actually pass a date in format YYYY-MM-DD HH:MM:SS for time reference. Use greater, after, later, smaller, before, till, until, on, equal to compare time \nnot, never for negation"
					new_rule = raw_input("ENTER 'q' to go back\n")
					if new_rule == "q":
						pass
					else:
						rules.add_new_rule(new_rule)
				
				elif edit_rules_choice == "3":
					print "\nENTER code corresponding to rule to remove it:"
					rules.print_current_rules()
					rule_code = raw_input("ENTER q to cancel\n")
					if rule_code == "q":
						pass
					else:
						rules.remove_rule(rule_code)


				elif edit_rules_choice == "4":
					print "\nENTER full file path:"
					rule_code = raw_input("ENTER q to cancel\n")
					if rule_code == "q":
						pass
					else:
						rules.update_rule_path(rule_code)

				elif edit_rules_choice == "5":
					break
				
				else:
					print "Please Enter valid Input"
					pass

		elif task_choice == "3":
			break
		else:
			print "Please Enter valid Input"