[![Python Versions](https://github.com/primetimetank21/tank-template/actions/workflows/python-versions.yml/badge.svg)](https://github.com/primetimetank21/tank-template/actions/workflows/python-versions.yml)

# Phissi👁n
## OVERVIEW
In this age of technology and information, Cyber Attacks are more common than ever before. So
many applications in use today ask for personal information, and sometimes users mistakenly
enter their sensitive credentials in non-legitimate applications. Reference [1] mentions that 91% of
all cyberattacks begin with some sort of phishing message [1].

Prior to the COVID-19 pandemic, phishing attacks were already common in the workplace
environment. Now that more people work from home, an increasing amount of communication is
conducted through digital mediums. With more people on their devices each day (i.e.,
smartphones, computers, tablets, etc.), users are more prone to Cyber Attacks.

Enter Phissi👁n. Phissi👁n is an application that helps its users make more informed decisions as it
relates to entering personal information. The aim of this software is to truly aid those that are
more susceptible to Cyber Attacks, primarily phishing attacks (i.e., older people, non-tech savvy
individuals, differently-abled individuals, etc.).

Phissi👁n seeks to implement a solution similar to the one mentioned in Reference [1]. It is
important to note that the authors never actually built this solution out, nor did they survey people
about their thoughts on the interface (i.e., ease of use, visual satisfaction, etc.). In order to
differentiate ourselves from these authors, we will use the following questions (and more) as
guidance:
  - Have you or someone you know ever downloaded malware/installed a virus?
  - Have you ever received a phishing email or text message before? How did you respond?
  - Would software like this actually be useful to you? Why or why not?
By interacting with the potential users of our application (via questions and surveys), we at
Phissi👁n hope to create a software that will be continuously used to aid in the fight against Cyber
Attacks.
## GOALS
1. Help all users (i.e., non-tech savvy individuals, visually impaired individuals, etc.) create
more informed decisions before entering sensitive information.
1. Increase overall awareness of Cyber Attacks.
1. Reduce the number of successful Cyber Attacks (primarily phishing attacks).

## HOW TO USE
### INSTALLATION
1. Clone this repository
    - ```git clone git@github.com:primetimetank21/phission.git```
1. Navigate to the cloned repository directory and create a virtual environment
    - `cd phission`
    - `python3 -m venv .venv`
1. Activate the environment and install the requirements
    - `source .venv/bin/activate`
    - `make install`
1. Start the [Pynecone](https://pynecone.io/) server
    - `pc run`