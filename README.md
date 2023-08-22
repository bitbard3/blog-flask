
# Minimal but super functional blog site made with flask 

[FlaskFolio](https://flaskfolio.onrender.com), minimalist design and functional aesthetics. Built using Flask and Bootstrap, it embodies the fusion of simplicity and efficiency.






## Features

- Authentication System
- Blog Management
- Pagination Handling
- Profile Customization
- Email-based Password Reset
- Responsive for vairious screen size

## Run Locally

Clone the project

```bash
  git clone https://github.com/bitbard3/blog-flask
```

Go to the project directory

```bash
  cd blog-flask
```

Build docker image

```bash
  docker build -t blog-flask .
```

Create and run the container

```bash
  docker run -d --name my-flask-container -p 3000:3000 blog-flask
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`MAIL_USER`

`MAIL_PASS`

`SECRET_KEY`

`SQLALCHEMY_DATABASE_URI`


## Lessons Learned

This project taught me lot about backend development, error handling,database management and I learnt a lot how internet works behind the scenes when i was deploying it to the internet I tried several deployment failed in few but it did taught a lot.


## Authors

- [@bitbard3](https://www.github.com/bitbard3)


## 🔗 Links
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/bitbard3)

