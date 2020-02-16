import os


def create_report(doctorId, userId):
    home_path = os.path.expanduser("~")
    user_folder = os.path.join(home_path, "HealthServer", "UserData", userId)
    doc_folder = os.path.join(user_folder, doctorId)

    if not (os.path.exists(doc_folder)):
        os.mkdir(doc_folder)
    try:
        file_path = os.path.join(doc_folder, "file.txt")

        file = open(file_path, "w")
        file.write("created")
        file.close()

        return 0
    except Exception as e:
        print(e)
