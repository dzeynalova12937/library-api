# Before Class: Set Up Your Laptop

Please finish this **before class**, because class time is for the activity and there won't be time to install software. It should take about 15 minutes.

**You will need:** a laptop (macOS, Windows or Linux) and an internet connection for the setup. Bring your laptop and charger to class.

## Step 1: Install the tools

Open a terminal (macOS: **Terminal**, Windows: **PowerShell**) and check what you already have:

| macOS / Linux | Windows |
|---|---|
| `python3 --version` | `py --version` |
| `git --version` | `git --version` |

Install anything that is missing:

- **Python 3.10 or newer:** [python.org/downloads](https://www.python.org/downloads/). On Windows, tick **"Add python.exe to PATH"** on the first installer screen.
- **Git:** [git-scm.com/downloads](https://git-scm.com/downloads). On macOS, you can instead accept the developer tools prompt that appears when you run `git --version`.
- **A code editor:** [Visual Studio Code](https://code.visualstudio.com/) is a good choice.
- **A GitHub account:** [github.com/signup](https://github.com/signup).

If you installed anything, close the terminal and open a new one before you continue.

If you have never used Git on this laptop, tell it who you are:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Step 2: Fork the repository

1. Open the class repository link from your instructor.
2. Click **Fork**, then **Create fork**. You now have your own copy on GitHub.

## Step 3: Clone your fork and install

On **your fork's** page, click **Code** and copy the HTTPS URL. It contains your username. Then run these commands one at a time, using your URL. Cloning creates the project folder for you.

**macOS / Linux:**

```bash
git clone https://github.com/YOUR-USERNAME/library-api.git
cd library-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell):**

```powershell
git clone https://github.com/YOUR-USERNAME/library-api.git
cd library-api
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

After activating, you should see `(.venv)` at the start of your terminal line.

## Step 4: Check that it worked

```bash
python -m unittest
```

The last lines should look like this, and then you're ready:

```text
Ran 53 tests in 0.200s

OK
```

The time will differ.

## If something goes wrong

| Problem | Fix |
|---|---|
| `python3`, `py` or `git` is not found | Install it (Step 1), then open a **new** terminal. |
| macOS asks to install developer tools | Accept and wait for it to finish. |
| `git clone` says the repository was not found | Copy the URL again from your fork's **Code** button. |
| Windows says running scripts is disabled when you activate | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again. |
| `(.venv)` doesn't appear | Make sure you're inside `library-api`, then run the activate command again. |
| `No module named flask` | Activate first (you should see `(.venv)`), then run `pip install -r requirements.txt`. |
| It still doesn't work | Send your instructor the command you ran and the full error message **before class**. |

## On the day of class

Open a terminal, go to your folder and activate it:

**macOS / Linux:**

```bash
cd library-api
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
cd library-api
.venv\Scripts\activate
```

## Saving your work to GitHub

Commit after each refactoring step that passes the tests:

```bash
git add .
git commit -m "Move the fine rule into its own function"
```

To upload your commits to your fork, open the `library-api` folder in VS Code, go to **Source Control** and click **Sync Changes**. Sign in to GitHub if VS Code asks. Plain `git push` in a terminal may reject your GitHub password, because GitHub doesn't accept passwords for pushing.
