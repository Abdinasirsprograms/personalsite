fetch('pull_articles/en')
.then(
    (data) => data.json()
    .then((data) => console.log(data)))