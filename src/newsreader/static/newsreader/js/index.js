const fetchData = class {
    constructor(){
        const content = {};
    };


    getData(){
        fetch('pull_articles/en').then(
            (response) => {    
                if(response.status === 200){
                    response.json()
                    .then(
                        (data) => {
                            this.handleResponse(data)
                        });
                }
            })
    };

    handleResponse(data){
        if(data){
            console.log(data)
            data.data["hiiraan.com"].forEach(element => {
                element.forEach(content => {
                    let createContent = document.createElement("div");
                    createContent.className = 'article'; 
                    console.log(content)
                    createContent.innerHTML += `[${content.site}] - ${content.title} - ${content.description} ${content.date_posted}`; 
                    document.querySelector('#article-container').appendChild(createContent); 
                })
            });
            data.data["dayniiile.com"].forEach(element => {
                element.forEach(content => {
                    let createContent = document.createElement("div");
                    createContent.className = 'article'; 
                    console.log(content)
                    createContent.innerHTML += `[${content.site}] - ${content.title} - ${content.description} ${content.date_posted}`; 
                    document.querySelector('#article-container').appendChild(createContent); 
                })
            });
            // console.log(data.data["hiiraan.com"]
            // );
        }
    };

};

const receivedData = new fetchData
receivedData.getData();