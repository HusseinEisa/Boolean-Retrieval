from django.shortcuts import render

# Create your views here.


def Search (request):
    Search = 0
    return render(request, "Search_Page.html", {'Query': Search})


def Result (request):
    
    # Define a variable to store Boolean Query 
    # Boolean_Query = input("Please, Enter the Boolean query at one line like that \"word1 and (word2 or not word3)\":\n")
    # Boolean_Query = "schizophrenia and not (approach or New)"
    Search = request.GET.get('Query')
    Boolean_Query = Search
    
    # Preparing Boolean Query's words 
    Boolean_Query = Preparing_Query(Boolean_Query)
    
    # Calculate the Result of Boolean Query
    Boolean_Query = Calc_Query(Boolean_Query)
    
    # change it from [[]] to []
    Boolean_Query = Boolean_Query[0]
    
    # Define a variable to store the number of results 
    Rank = 0
    DN = []
    DT = []
    
    for Term in range(len(Boolean_Query)):
        if True not in Boolean_Query:
            break
        if (Boolean_Query[Term] == True):
            DN.append(Term+1)
            DT.append(Documents[Term])
            Rank += 1
    
    context = {
        'Boolean_Query': Boolean_Query,
        'Search': Search,
        'Rank': Rank,
        'DN': DN,
        'DT': DT,
    }
    return render(request, "Search_Page.html", context)




# Preparing Documents [Remove none alphabetic charts] [Make all words in upper case]
def Preparing_Documents (Document):
    for Sub_String in range(len(Document)):
        Document[Sub_String] = Document[Sub_String].upper()
        for Letter in Document[Sub_String]:
            if Letter.isalpha() or Letter.isspace():
                continue
            else:
                Document[Sub_String] = Document[Sub_String].replace(Letter,"")
    
    return Document

# Preparing Boolean Query [Remove none alphabetic charts except normal brackets "()"] [Make all words in upper case] [operators {and / or / not / and not / or not}]
def Preparing_Query (Str_Query):
    
    # Preparing brackets before spliting the Str_Query
    Str_Query = Str_Query.replace("(","( ")
    Str_Query = Str_Query.replace(")"," )")
    
    # Split the Str_Query to single words and operators and brackets
    Str_Query = Str_Query.upper().split(" ")
    
    # Remove none alphabetic charts from Str_Query's words except normal brackets "()"
    for Q in range(len(Str_Query)) :
        for Letter in Str_Query[Q]:
            if Letter.isalpha() or Letter.isspace() or Letter=="(" or Letter==")":
                continue
            else:
                Str_Query[Q] = Str_Query[Q].replace(Letter,"")
    
    # Define a list to store the Terms of words and operators
    Query = []
    
    # Convert the words to Boolean Terms from "Term_Incidence_Matrix" and store them in Query list with operators
    for S in range(len(Str_Query)):
        if (Str_Query[S-1]=="AND" or Str_Query[S-1]=="OR") and Str_Query[S]=="NOT":
            Query[-1] = Query[-1]+" NOT"
        elif Str_Query[S]=="AND" or Str_Query[S]=="OR" or Str_Query[S]=="NOT" or Str_Query[S]=="(" or Str_Query[S]==")":
            Query.append(Str_Query[S])
        elif Str_Query[S] in Term_Incidence_Matrix:
            Query.append(Term_Incidence_Matrix[Str_Query[S]])
        else:
            Query.append([False]*Doc_Numbers)
    
    return Query

# Function to Calculate the result of Boolean Query
def Calc_Query (Query):
    
    # if statement to calc what in the brackets at first
    if "(" in Query :
        Insert = Calc_Query(Query[Query.index("(")+1:Query.index(")")])
        Query.insert(Query.index("("), Insert)
        Query = [x for x in Query if x not in Query[Query.index("("):Query.index(")")+1]]
        Query[Query.index(Insert)] = Insert[0]
    
    # calc (not) operator
    if "NOT" in Query :
        for X in range(Doc_Numbers):
            Query[Query.index("NOT")+1][X] = not Query[Query.index("NOT")+1][X]
        Query.remove("NOT")
    
    for Doc in range(Doc_Numbers):
        for Key in Query:
            
            # if statement to skip Operators words of Boolean Query
            if Query[Query.index(Key)] == "AND" or Query[Query.index(Key)] == "OR" or Query.index(Key) == 0:
                continue
            
            # calc (and) operator
            elif Query[Query.index(Key)-1] == "AND":
                for N in range(Doc_Numbers):
                    Query[Query.index(Key)-2][N] = Query[Query.index(Key)-2][N] and Query[Query.index(Key)][N]
                Query.remove("AND")
                # Query.remove(Query[Query.index(Key)])
            
            # calc (and not) operator
            elif Query[Query.index(Key)-1] == "AND NOT":
                for N in range(Doc_Numbers):
                    Query[Query.index(Key)-2][N] = Query[Query.index(Key)-2][N] and not Query[Query.index(Key)][N]
                Query.remove("AND NOT")
                # Query.remove(Query[Query.index(Key)])
            
            # calc (or) operator
            elif Query[Query.index(Key)-1] == "OR":
                for N in range(Doc_Numbers):
                    Query[Query.index(Key)-2][N] = Query[Query.index(Key)-2][N] or Query[Query.index(Key)][N]
                Query.remove("OR")
                # Query.remove(Query[Query.index(Key)])
            
            # calc (or not) operator
            elif Query[Query.index(Key)-1] == "OR NOT":
                for N in range(Doc_Numbers):
                    Query[Query.index(Key)-2][N] = Query[Query.index(Key)-2][N] or not Query[Query.index(Key)][N]
                Query.remove("OR NOT")
                # Query.remove(Query[Query.index(Key)])
    
    return Query


# Define a variable to store the number of documents
# Doc_Numbers = int(input("Please, Enter the number of documents: "))
Doc_Numbers = 4

# Define a list to store documents on it
# Documents = []
Documents = [
    "breakthrough drug for schizophrenia",
    "new schizophrenia drug",
    "new approach for treatment of schizophrenia",
    "new hopes for schizophrenia patients"
]

# Take the documents from user
# for i in range(Doc_Numbers):
#     print("Please, Enter the document number",i+1,"(write it in one line)")
#     Documents.append(input())

# Preparing document's words 
Documents = Preparing_Documents(Documents)

# Define a dectionary for Term Incidence Matrix
Term_Incidence_Matrix = {}

# Store words and terms in Term Incidence Matrix [Make all terms equal 0 at start]
for Doc in Documents:
    for Word in Doc.split(" "):
        if Word in Term_Incidence_Matrix:
            continue
        else:
            Term_Incidence_Matrix.update({f'{Word}' : [False]*Doc_Numbers})

# Store the real true Terms in Term Incidence Matrix
for row in Term_Incidence_Matrix:
    for col in range(Doc_Numbers):
        if row in Documents[col]:
            Term_Incidence_Matrix[row][col] = True


