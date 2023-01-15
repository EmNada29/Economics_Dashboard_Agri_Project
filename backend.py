import sqlite3

class Database:
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS pse (id INTEGER PRIMARY KEY, Nom_Exploitation TEXT, "
                    "SIREN INTEGER, Annee INTEGER, SAU INTEGER, INDICATEUR1 INTEGER,INDICATEUR2 INTEGER,INDICATEUR3 INTEGER,"
                         "INDICATEUR1_score INTEGER,INDICATEUR2_score INTEGER,INDICATEUR3_score INTEGER)")
        self.conn.commit()

    def insert(self,Nom_Exploitation, SIREN, Annee, SAU, INDICATEUR1, INDICATEUR2, INDICATEUR3, INDICATEUR1_score, INDICATEUR2_score, INDICATEUR3_score):
        #the NULL parameter is for the auto-incremented id
        self.cur.execute("INSERT INTO pse VALUES(NULL,?,?,?,?,?,?,?,?,?,?)", (Nom_Exploitation,SIREN,Annee, SAU, INDICATEUR1, INDICATEUR2, INDICATEUR3, INDICATEUR1_score, INDICATEUR2_score, INDICATEUR3_score))
        self.conn.commit()


    def view(self):
        self.cur.execute("SELECT * FROM pse")
        rows = self.cur.fetchall()

        return rows

    def search(self,Nom_Exploitation="", SIREN="", Annee="", SAU="", INDICATEUR1="", INDICATEUR2="", INDICATEUR3="", INDICATEUR1_score="", INDICATEUR2_score="", INDICATEUR3_score=""):
        self.cur.execute("SELECT * FROM pse WHERE Nom_Exploitation = ? OR SIREN = ? OR Annee = ? OR SAU = ? OR INDICATEUR1 = ? OR INDICATEUR2 = ? OR INDICATEUR3 = ? OR INDICATEUR1_score = ? OR INDICATEUR2_score = ? OR INDICATEUR3_score = ?",
                     (Nom_Exploitation, SIREN, Annee, SAU, INDICATEUR1, INDICATEUR2, INDICATEUR3, INDICATEUR1_score, INDICATEUR2_score, INDICATEUR3_score))
        rows = self.cur.fetchall()
        #conn.close()
        return rows

    def delete(self,id):
        self.cur.execute("DELETE FROM pse WHERE id = ?", (id,))
        self.conn.commit()
        #conn.close()

    def update(self,id, Nom_Exploitation,SIREN,Annee, SAU, INDICATEUR1, INDICATEUR2, INDICATEUR3, INDICATEUR1_score, INDICATEUR2_score, INDICATEUR3_score):
        self.cur.execute("UPDATE pse SET Nom_Exploitation = ?, SIREN = ?, Annee = ?, SAU = ?, INDICATEUR1 = ?, INDICATEUR2 = ?, INDICATEUR3 = ?, INDICATEUR1_score = ?, INDICATEUR2_score = ?, INDICATEUR3_score = ? WHERE id = ?",
                         (Nom_Exploitation,SIREN,Annee, SAU, INDICATEUR1, INDICATEUR2, INDICATEUR3, INDICATEUR1_score, INDICATEUR2_score, INDICATEUR3_score, id))
        self.conn.commit()


    #Pas besoin de ce détail, c'est du perfectionnement
    # def refactor_id(self,id):
    #    self.cur.execute("UPDATE pse SET id = ?",(id-1,))
    #    self.conn.commit()

    #destructor-->now we close the connection to our database here
    def __del__(self):
        self.conn.close()



#Documentation : https://sql.sh/cours/select
