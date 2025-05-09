===========================================
🧠 MEMORY TASK APPLICATION - INSTRUCTIONS
===========================================

📦 What's Included:
-------------------
You should have the following files/folders inside the extracted folder:

- main.exe                  ← The application you will run
- images/                   ← Contains all experimental images
- result_output/            ← Where participant data will be saved
- README.txt                ← This instruction file

🖥️ How to Run the Application:
-------------------------------
1. Double-click `main.exe` to launch the task.
2. A dialog box will appear asking for:
   - Subject ID (e.g., sub01)
   - Session Number (e.g., 1)
   - Task Mode (choose "self_paced" or "fixed")

3. If a data file for that subject/session already exists, the program will ask whether to overwrite it.

4. The memory task will then begin. The participant will see a series of images and respond using the keyboard:
   - Press **B** if the item is **NEW**
   - Press **N** if the item is **OLD**
   - Press **M** if the item is **SIMILAR**

5. After completing the task, the program will automatically return to the initial screen to allow entry for the next participant.

📁 Where to Find the Experimental Data:
----------------------------------------
All session data are saved in the `result_output/` folder under each participant’s subfolder.  
For example:

    result_output/
    └── sub01/
        └── session_1_self_paced.csv

📄 CSV File Format Explanation:
-------------------------------
Each `.csv` file contains a row for each trial and includes the following columns:

- trial         → Trial number
- image         → Image filename shown
- type          → Trial type: 'old', 'similar', or 'new'
- expected      → Expected correct response label ('N', 'O', or 'M')
- response      → Actual key pressed by participant ('N', 'O', 'M', or 'F' for no response)
- correct       → Whether the response was correct (1 = correct, 0 = incorrect, 'F' = no response)

✅ Tip: Always double-check that a `.csv` file was created after each session!

📬 Questions or bugs?
---------------------
Contact the developer if you have any issues or questions running the application.
