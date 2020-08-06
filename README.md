![github version](https://d25lcipzij17d.cloudfront.net/badge.svg?id=gh&type=6&v=1.1.1&x2=0)
# Hipposcraper

## Create Directory Skeletons and READMEs for Holberton School Projects

This repo is now being maintained by [Patrick DeYoreo](github.com/patrickdeyoreo).
Feel welcome to get in touch with any questions, comments, contributions, or
criticisms. If you would like to contribute, you should totally do that! Take a
look at the source code and send me a message (either on Slack or by email) or
submit a pull request and I'll check it out. I assure you there is much to do.

<p align="center">
  <img src="http://www.holbertonschool.com/holberton-logo.png">
</p>

The Hipposcraper automates file template creation for Holberton projects. The 
program takes a Holberton School project URL, scrapes the webpage, and creates
the corresponding directory and files. The Hipposcraper supports the following: 

| System Engineering    | Low-Level Programming | Higher-Level Programming      |
| --------------------- | --------------------- | ----------------------------- |
| Bash script templates | `.c` templates        | `.py` and `.c` templates      |
|                       | Header file           | Header file                   |
|                       | `_putchar` file       |                               |
|                       | `main.c` test files   | `main.c`/`main.py` test files |
| `README.md`           | `README.md`           | `README.md`                   |

---

## Getting Started :wrench:

### Prerequisites

The Hipposcraper depends on the Python packages `requests` and `beautifulsoup4`. 
The simplest way to install these packages is through `pip`.
If `pip` is not installed, you may install it by running whichever of the
following commands applies to you.

##### On Arch Linux:

```
sudo pacman -S python-pip
```

##### On Debian and Ubuntu:

```
sudo apt install python3-pip
```

##### On CentOS and RHEL:

```
sudo yum install epel-release 
sudo yum install python-pip
```

##### On Fedora:

```
sudo dnf install python3
```

##### On OpenSUSE:

```
sudo zypper install python3-pip
```

Once `pip` available, install `requests` and `beautifulsoup4` as follows:

```
pip install --user -r requirements.txt
```

Note that you may need to run the `--user` option when installing these packages.


### Installation

Clone the repository:

```
git clone https://github.com/patrickdeyoreo/hipposcraper
```

Enter the project directory:

```
cd hipposcraper
```

Run the setup script:

```
python3 setup.py install --user
```

### Setup :key:

**Setting User Information**

After cloning a local copy of the repository, enter your Holberton intranet 
username and password as well as your GitHub name, username, and profile link 
in a `credentials.json` file.
  - **Using `setup.sh`: Run `./setup.sh` to automatically setup the required information**

**Setting Aliases**

The Hipposcraper defines two separate Python scripts - one 
([hippodir.py](./hippodir.py)) that creates projects, 
and a second ([hippodoc.py](./hippodoc.py)) that creates 
`README.md` files. To run both simultaneously, you'll need to define an alias 
to the script [hipposcraper.sh](./hipposcraper.sh).

First, open the script and enter the full pathname to the Hipposcraper 
directory where directed. Then, if you work in a Bash shell, define the 
following in your `.bashrc`:

```
alias hipposcraper='./ENTER_FULL_PATHNAME_TO_SCRAPER_DIRECTORY_HERE/hipposcraper.sh'
```

Alternatievely, you can define separate aliases for each individual script. To 
define a project scraper alias:

```
alias hippodir='./ENTER_FULL_PATHNAME_TO_SCRAPER_DIRECTORY_HERE/hipposcraper.py'
```

And to define a `README.md` scraper alias:

```
alias hippodoc='./ENTER_FULL_PATHNAME_TO_SCRAPER_DIRECTORY_HERE/hippodoc.py'
```

*NOTE: This program only works with Python 2; ensure that your aliases 
specify 'python2' (Mechanize is not supported by Python 3).*

---

## Usage :computer:

After you have setup the proper aliases, you can run the Hipposcraper with the 
following command:

```
~$ hipposcraper project_link
```

Where `project_link` is the URL link to the Holberton School project to scrape.

Alternatively, to run only the project scraper:

```
~$ hippodir project_link
```

Or only the `README.md` scraper:

```
~$ hippodoc project_link
```

### `check.sh` - Generated for checking formats on all required files

```
~$ ./check.sh
```

## Repository Contents :file_folder:

* [hipposcraper.sh](./hipposcraper.sh)
  * A Bash script for running the entire Hipposcraper at once.

* [hippodir.py](./hippodir.py)
  * Python script that scrapes Holberton intranet webpage to create project 
directories.

* [hippodoc.py](./hippodoc.py)
  * Python script that scrapes Holberton intranet webpage to create project 
`README.md`.

* [credentials.json](./credentials.json)
  * Stores user Holberton intranet and GitHub profile information.

* [scrapers](./scrapers)
  * Folder of file-creation scrapers.
    * [base_parse.py](./scrapers/base_parse.py): Python script for parsing project pages.
    * [sys_scraper.py](./scrapers/sys_scraper.py): Python methods for creating 
Bash task files for system engineering projects.
    * [low_scraper.py](./scrapers/low_scraper.py): Python methods for creating 
`_putchar.c`, task files, and header file for low-level programming projects.
    * [high_scraper.py](./scrapers/high_scraper.py): Python methods for creating 
Python task files for higher-level programming projects.
    * [test_file_scraper.py](./scrapers/test_file_scraper.py): Python methods for creating 
test files for all project types.
* [setup.sh](./setup.sh): Sets up all variables and aliases with this script.
* [autover.sh](./autover.sh): Development tool for changing all version strings.
    
---

## Example of the C scraper

![demo0](https://i.imgur.com/oB08uzF.png)

## Example of the README scraper

![demo1](https://i.imgur.com/6qaC92l.jpg)

## Example of `check.sh`

![demo2](https://i.imgur.com/oQqTLWXh.jpg)

---

## Authors
* **Derrick Gee** - [kai-dg](https://github.com/kai-dg)
* **Patrick DeYoreo** - [patrickdeyoreo](https://github.com/patrickdeyoreo)

---

## Contributors
* **Brennan D Baraban** - [bdbaraban](https://github.com/bdbaraban)
* **Carlos Daniel Cortez** - [kael1706](https://github.com/kael1706)
