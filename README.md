# Hipposcraper

## Create Directory Skeletons and READMEs for Holberton School Projects

This repo is currently maintained by [Patrick DeYoreo](github.com/patrickdeyoreo).
Feel welcome to get in touch with any questions, comments, contributions, or
criticisms. If you would like to contribute, you should totally do that! Check
out the source code and send me a message (either on Slack or by email), or
make some changes and submit a pull request.

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

First, install `pip`:

#### On Arch Linux:

```
sudo pacman -S python-pip
```

#### On Debian and Ubuntu:

```
sudo apt install python3-pip
```

#### On Fedora:

```
sudo dnf install python3
```

Next, ensure `setuptools` is up-to-date:

```
python3 -m pip install --user -U setuptools
```

### Installation

Clone the repository:

```
git clone https://github.com/patrickdeyoreo/hipposcraper
```

Run the installation script:

```
hipposcraper/install.py
```

---

## Usage :computer:

To run the Hipposcraper, use following command, where `URL` is the URL of a
project on the Holberton intranet:

```
hipposcraper URL
```

Alternatively, run only the project scraper:

```
hippodir URL
```

Or run only the `README.md` scraper:

```
hippodoc URL
```

Or simply configure user credentials:

```
hippoconfig
```

---

## Repository Contents :file\_folder:

* [hipposcraper.py](./hipposcraper.py) -
  run the hipposcraper

* [hippodir.py](./hippodir.py) -
  create project skeleton

* [hippodoc.py](./hippodoc.py) -
  create project documentation

* [hippoconfig.py](./hippoconfig.py) -
  manage user configuration

* [scrapers](./hipposcraper/scrapers) -
  folder of file-creation scrapers

  - [base\_parse.py](./hipposcraper/scrapers/base_parse.py) -
    parse project information

  - [sys\_scraper.py](./hipposcraper/scrapers/sys_scraper.py) -
    create task files for system engineering projects

  - [low\_scraper.py](./hipposcraper/scrapers/low_scraper.py) -
    create task files and header file for low-level programming projects

  - [high\_scraper.py](./hipposcraper/scrapers/high_scraper.py) -
    create task files for higher-level programming projects

  - [test\_file\_scraper.py](./hipposcraper/scrapers/test_file_scraper.py) -
    create test files for all project types

* [setup.py](./setup.py) -
  `setuptools` installation script

* [install.py](./install.py) -
  alternate installation script

* [autover.sh](./autover.sh) -
  tool for changing all version strings

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
