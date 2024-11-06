import subprocess
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # Cache le message de pygame

def installer_bibliotheques_si_besoin(bibliotheques : list[str]):
    """
    Vérifie si les bibliothèques sont installées et les installe si nécessaire.
    bibliotheques: Liste des bibliothèques à installer
    """

    for lib in bibliotheques:
            if lib == "opencv-python":
                try:
                    import cv2
                except ImportError:
                    print(f"Installation de la bibliothèque {lib}...")
                    subprocess.check_call(["pip", "install", lib])
            else:
                try:
                    __import__(lib)
                except ImportError:
                    print(f"Installation de la bibliothèque {lib}...")
                    subprocess.check_call(["pip", "install", lib])


# Liste des bibliothèques à installer si elles ne sont pas déjà installées
bibliotheques_a_installer = ["pygame", "opencv-python", "moviepy"]

if __name__ == "__main__" :
    # Appel de la fonction pour installer les bibliothèques si nécessaire
    installer_bibliotheques_si_besoin(bibliotheques_a_installer)