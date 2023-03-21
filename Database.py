import pyodbc as odcb

SERVER_NAME = 'GHASSANYJR'
DATABASE_NAME = 'Transcription Analysis'

# Create the connection to SQL SERVER
conn = odcb.connect('Driver={SQL Server};'
                      'Server=GHASSANYJR;'
                      'Database=Transcription Analysis;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

# CREATE tables in the SQL SERVER
# cursor.execute('''
# 		CREATE TABLE Authorisation (
# 			Token_ID varchar(100) NOT NULL,
#             Org_ID VARCHAR(50) CHECK (LEFT(Org_ID, 3) = 'org' AND ISNUMERIC(SUBSTRING(Org_ID, 4, LEN(Org_ID) - 3)) = 1) NOT NULL,
#             UNIQUE (Org_ID),
#             PRIMARY KEY (Org_ID)
# 		)
# ''')

# cursor.execute('''
# 		CREATE TABLE Request (
# 			Request_ID varchar(255) NOT NULL,
#             Audio_URL varchar(2048) NOT NULL,
#             Sentiment_Distribution_Pos float NOT NULL,
#             Sentiment_Distribution_Neg float NOT NULL,
#             highest_Count int NOT NULL,
#             Date varchar(10) NOT NULL,
# 	        UNIQUE (Request_ID),
# 	        PRIMARY KEY (Request_ID),
#             Org_ID VARCHAR(50) FOREIGN KEY REFERENCES Authorisation(Org_ID)
# 		)
# ''')

# cursor.execute('''
# 		CREATE TABLE Words (
# 			Word_ID int NOT NULL,
#             Word varchar(255) NOT NULL,
#             IsSensitive bit NOT NULL,
#             Word_Count int NOT NULL,
#             Request_ID varchar(255) FOREIGN KEY REFERENCES Request(Request_ID),
#             UNIQUE (Word_ID),
#             PRIMARY KEY (Word_ID)
# 		)
# ''')

# cursor.execute('''
# 		CREATE TABLE Conversations (
# 			Conversation_ID int NOT NULL,
#             Sender varchar(255) NOT NULL,
#             Content varchar(max) NOT NULL,
#             Sentiment varchar(8) NOT NULL,
#             Confidence float NOT NULL,
#             Comment varchar(max) NULL,
#             Request_ID varchar(255) FOREIGN KEY REFERENCES Request(Request_ID),
#             UNIQUE (Conversation_ID),
#             PRIMARY KEY (Conversation_ID),
# 		)
# ''')
# conn.commit()

# ALTER Data in Database
# alter_statement = "ALTER TABLE Conversations ADD CONSTRAINT Sentiment CHECK (Sentiment IN ('POSITIVE', 'NEGATIVE'))"
# cursor = conn.cursor()
# cursor.execute(alter_statement)
# conn.commit()






