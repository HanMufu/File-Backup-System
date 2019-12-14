# RUBackup

This is the course project of Rutgers CS552 Computer Networks. Our project, RU_Backup implemented a online file backup system.

## Dependencies

* Python == 3.7.3
* PySide2 == 5.13.2
* paramiko == 2.7.1
* qdarkstyle == 2.7
* pymysql == 0.9.3
* PyQt5 ==  5.9.2

## Usage

First, install all the dependencies in  `./src/requirements.txt` 

	$ cd src
	$ pip install requirements.txt

Then, just execute the UI file
	
	$ python window.py

Users could login to the existed account or click the sign up button to sign up for a new account.

After the account verified or new account created, you get into the main frame.

In the main frame, you could double-click the folder item in the list to get into the next level directory. You could push the back button to get back to parent directory. You could use the icons to dowanload the file or folder, and check the information of file or folder. The combo box presents all the versions of your backup, you could check the contents of each version by just clicking the item in the combo list.

## Example

![image](https://github.com/HanMufu/RUBackup/raw/master/images-folder/Snipaste_2019-12-13_23-33-49.png)
![image](https://github.com/HanMufu/RUBackup/raw/master/images-folder/Snipaste_2019-12-13_23-34-21.png)
![image](https://github.com/HanMufu/RUBackup/raw/master/images-folder/Snipaste_2019-12-13_23-34-26.png)
