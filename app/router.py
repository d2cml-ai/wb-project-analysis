import re

projectNumberPattern = re.compile(r"\D(P\d{6})\D")
reportNumberPattern = re.compile(r"\D(PAD\d{3,4}|PP\d{3,4})\D")
specialCasePattern = re.compile(r"\D(\d{5,6})\D")
specialCases = [
        '153807', '150976', '00000', '83270', '90483', '87051',
        '126142', '120729', '126123', '126148', '177898'
]

def detectDocumentQuery(query):
        paddedQuery = " " + query + " "
        paddedQuery = paddedQuery.upper()
        foundProjectIds = projectNumberPattern.findall(paddedQuery)
        foundReportNumbers = reportNumberPattern.findall(paddedQuery)
        foundSpecialCases = specialCasePattern.findall(paddedQuery)

        if len(foundProjectIds) > 0:
                return foundProjectIds[0]
        if len(foundReportNumbers) > 0:
                return foundReportNumbers[0]
        if len(foundSpecialCases) > 0:
                if foundSpecialCases[0] in specialCases:
                        return foundSpecialCases[0]
        return False

# def main():
#         userInput = ""
#         while userInput != "exit":
#                 userInput = input("Query: ")
#                 routerResult = routQuery(userInput)
#                 print(routerResult)
                

# if __name__ == "__main__":
#         main()