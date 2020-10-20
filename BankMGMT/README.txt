MODULES SETUP
-------------------------
pip install pipenv
pipenv shell
cd <path\To\Directory>
pipenv install		-----> inside BankMGMT (same directory as readme)
-------------------------
##____INSTRUCTIONS___##
1) python SqlSetupV2	-----> inside pipenv shell
2)python main.py	-----> inside pipenv shell

-------------------------
##_________NOTE________##
1) For localhost leave blank
NOTE: a) Will create a new database called BANKMGMT in root
      b) DONOT open .csv files in MS excel (they change the datetime format from YYYY/MM/DD to DD/MM/YYYY)
      c) Open .csv in notepad
2) For password and Acno refer ProfileData
Eg: 1,Shea Scapelhorn,1971-03-10,CN,5PbQNiN6,Daqiao,072 Shasta Court,1552704955,SV,None,+86 731 255 9250,Female
					^				  ^
					^				  ^
				     Password				 Acno
