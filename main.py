import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io
# importing the modules.

def get_github_profile_info(profile_link):
    username = profile_link.split('/')[-1]
    api_url = f'https://api.github.com/users/{username}'
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Error", f"Unable to fetch data from GitHub API. Status code: {response.status_code}")
        return None

def show_github_profile_info():
    profile_link = entry_link.get().strip()

    if not profile_link:
        messagebox.showerror("Error", "Please enter your GitHub profile link.")
        return

    profile_info = get_github_profile_info(profile_link)

    if profile_info:
        avatar_url = profile_info['avatar_url']
        avatar_data = requests.get(avatar_url).content
        avatar_image = Image.open(io.BytesIO(avatar_data))
        avatar_image.thumbnail((100, 100))  # Resize the image if needed
        avatar_photo = ImageTk.PhotoImage(avatar_image)
        avatar_label.config(image=avatar_photo)
        avatar_label.image = avatar_photo

        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Username: {profile_info['login']}\n")
        result_text.insert(tk.END, f"Name: {profile_info['name']}\n")
        result_text.insert(tk.END, f"Bio: {profile_info['bio']}\n")
        result_text.insert(tk.END, f"Number of public repositories: {profile_info['public_repos']}\n")
        result_text.insert(tk.END, f"Number of followers: {profile_info['followers']}\n")
        result_text.insert(tk.END, f"Number of following: {profile_info['following']}\n")
        result_text.insert(tk.END, f"GitHub URL: {profile_info['html_url']}\n")
        result_text.config(state=tk.DISABLED)
    else:
        avatar_label.config(image='')
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("GitHub Profile Info")

    # Style
    s = ttk.Style()
    s.configure('TLabel', font=('Helvetica', 12))
    s.configure('TButton', font=('Helvetica', 12))
    s.configure('TEntry', font=('Helvetica', 12))

    label_link = ttk.Label(root, text="Enter your GitHub profile link:")
    label_link.pack(pady=5)

    entry_link = ttk.Entry(root, width=40)
    entry_link.pack(pady=5)

    btn_fetch_info = ttk.Button(root, text="Fetch Info", command=show_github_profile_info)
    btn_fetch_info.pack(pady=10)

    avatar_label = ttk.Label(root)
    avatar_label.pack(pady=10)

    result_text = tk.Text(root, width=60, height=15, font=('Helvetica', 12), state=tk.DISABLED)
    result_text.pack(pady=10)

    root.mainloop()
