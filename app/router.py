import re

numbersPattern = re.compile(r"\d+")

def detectQueryType(query):
        foundNumberStrings = numbersPattern.findall(query)
        
        if len(foundNumberStrings) == 0:
                return False
        
        numberStringLengths = [len(number) for number in foundNumberStrings]

        try:
                projectIdIndex = numberStringLengths.index(7)
        except ValueError:
                return False
        
        projectId = "P" + foundNumberStrings[projectIdIndex]
        return projectId

# def main():
#         userInput = ""
#         while userInput != "exit":
#                 userInput = input("Query: ")
#                 routerResult = routQuery(userInput)
#                 print(routerResult)
                

# if __name__ == "__main__":
#         main()