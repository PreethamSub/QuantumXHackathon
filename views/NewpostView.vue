<template>
    <main>
        <nav style="background-color: rgb(59, 19, 96)" class="navbar navbar-expand-lg">
        <a class="navbar-brand" href="#">AI Blogger</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
            <li class="nav-item">
                <a class="nav-link" @click="postDataToWordpress()" href="#">Post on Wordpress</a>
            </li>
            </ul>
        </div>
        </nav>
       <div>
            <div class="row">
                <div class="col-lg-6" id="editPanel">
                    <div v-if="!isLoading" id="chooser">
                        <h5>Choose an heading</h5>
                        <span v-bind:class="(this.selectedData.heading==heading.content)?'low_opacity':'high_opacity'" @click="selectHeading(heading.content)" v-for="heading in apiData.headings">
                            <button class="heading-item">{{ heading.content }}</button>
                        </span>
                        <div class="custom-heading">
                            <span style="margin-left: 1vw;">Heading : </span>
                            <input type="text" v-model="selectedData.heading" placeholder="Custom Heading">
                        </div>
                        <h5>Paragraph content</h5>
                        <textarea v-model="apiData.content" cols="60" rows="7"></textarea>
                        <h5>Choose an Image</h5>
                        <span v-bind:class="(this.selectedData.image==image.url)?'low_opacity':'high_opacity'" @click="selectImage(image.url)" v-for="image in apiData.images">
                            <img class="chooser_img" v-bind:src="image.url">
                        </span>
                        <div style="margin-top: 2vh;">
                            <button @click="addToArticle()">Add to article</button>
                        </div>
                        
                    </div>
                    <div v-if="isLoading" id="loadingView">
                        <div class="spinner-container">
                            <div class="spinner"></div>
                            <p>Loading...</p>
                        </div>
                        <!-- loading -->
                    </div>
                    <div id="prompt">
                        <h5>AI Generator</h5>
                        <input type="text" v-model="prompt" placeholder="Enter prompt here">
                        <button @click="callAPI()">Go</button>
                    </div>
                </div>
                <div class="col-lg-6" id="previewPanel">
                    <div v-for="articleValue in articleData" v-id="articleValue.id">
                        <div class="preview_heading" v-if="articleValue.type == 'HEADING'"><h2>{{ articleValue.content }}</h2></div>
                        <div class="preview_text" v-if="articleValue.type == 'TEXT'">{{ articleValue.content }}</div>
                        <div class="text-center" v-if="articleValue.type == 'IMAGE'"><img class="image_preview" v-bind:src=articleValue.url alt="image"></div>
                    </div>
                </div>
            </div>
       </div>
    </main>
</template>

<script>
    import axios from "axios"
    export default {
        data(){
            return {
                prompt:"",
                apiData : {
                    headings : [
                    ],
                    content : "",
                    images : []
                },
                articleData:[
                    // {id: 1, type: 'HEADING', content: 'Software engineering'},
                    // {id: 2, type: 'TEXT', content: 'software engineer is a person who applies engineer…lso be written in a low-level assembly language .'},
                    // {id: 3, type: 'HEADING', content: 'Python (programming language)'},
                    // {id: 4, type: 'TEXT', content: 'Python is dynamically typed and garbage-collected … stepped down from the position on 12 July 2018 .'},
                    // {id: 5, type: 'IMAGE', url: 'https://upload.wikimedia.org/wikipedia/commons/6/66/Guido_van_Rossum_OSCON_2006.jpg'}  
                ],
                selectedData:{
                    heading : "",
                    image : ""
                },
                currId : 0,
                isLoading : false,
                currWaitTime : 30
            }
        },
        methods:{
            callAPI : async function(){
                this.isLoading = true;
                let response = await axios.post("http://172.21.21.170:5000/generate" , {prompt : this.prompt});
                console.log(response)
                if(response.data.headings.length > 3)
                    this.apiData.headings = response.data.headings.slice(0 , 3);
                else
                    this.apiData.headings = response.data.headings
                if(response.data.images.length > 3)
                    this.apiData.images = response.data.images.slice(0 , 3);
                else
                    this.apiData.images = response.data.images
                this.apiData.content = response.data.content;
                this.isLoading = false;
            },
            selectHeading : function(heading){
                this.selectedData.heading = heading;
            },
            selectImage : function(image){
                this.selectedData.image = image;
            },
            addToArticle(){
                if(this.selectedData.heading != ""){
                    this.articleData.push({id : this.currId+1 , type : "HEADING" , content : this.selectedData.heading});
                    this.selectedData.heading = "";
                    this.currId+=1;
                }
                if(this.apiData.content != ""){
                    this.articleData.push({id : this.currId+1 , type : "TEXT" , content : this.apiData.content});
                    this.apiData.content = "";
                    this.currId+=1;
                }
                if(this.selectedData.image != ""){
                    this.articleData.push({id : this.currId+1 , type : "IMAGE" , url : this.selectedData.image});
                    this.selectedData.image = "";
                    this.currId+=1;
                }
            },
            postDataToWordpress() {
                var title;
                var isHeadingFound = false;
                this.articleData.forEach(element => {
                    if(element.type == "HEADING" && !isHeadingFound){
                        isHeadingFound = true;
                        title = element.content;
                    }
                });
                axios.post("http://172.21.21.170:5000/wordpress" , {articleData : this.articleData , title : title});
            }
        }
    }
</script>

<style>
 @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;500;600&display=swap');

    *{
    font-family: 'Poppins', sans-serif;
    }
    #editPanel{
        background-color: #e8e8e8;
    }
    #chooser{
        margin-left: 2vw;
        margin-top: 1vh;
        /* position: fixed; */
    }

    input{
    height: 5vh;
    background-color: #F1F1F1;
    border: 1px solid #656565;
    color: #656565;
    border-radius: 10px;
    width: 30vw;
    margin: 1vw;
    box-shadow:2px 2px 0 0 #aeaeae;
    background: #fff;
  }

  #prompt{
   text-align: center;
   /* position: fixed;
   top: 85vh;
   left : 6vw; */
  }
  button{
    color: white;
    background-color: rgb(134, 46, 216);
    padding: 1vh 1.5vw;
    border: none;
    border-radius: 10px;
  }
  h5{
    margin-top: 2vh;
  }
  textarea{
    border: none;
    border-radius: 10px;
    width: 40vw;
  }

  .heading-item{
    background-color: #bbbbbb;
    padding: 1vh;
    border-radius: 5px;
    margin-bottom: 1vh;
    margin-top: 2vh;
    margin-right: 1vw;
    color: black;
  }

  .chooser_img{
    width: 11vw;
    height: 11vw;
    margin-right: 2vw;
    background-color: #e8e8e8;
  }
  .low_opacity{
    opacity: 0.5;
  }
  .high_opacity{
    opacity: 1;
  }
  .image_preview{
    max-height: 40vh;
    max-width: 50vw;
    text-align: center;
  }
  .preview_heading{
    margin: 1vw 1vh;
  }
  .preview_text{
    margin: 2.5vh 1vw;
  }

  .spinner-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 90vh;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left: 4px solid rgb(134, 46, 216);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

.custom-heading{
    margin : -1vw;
}

.navbar-brand{
    padding: 0 20px;
    color: white;
}

.nav-link{
    color: white;
}

.nav-link:hover{
    color: wheat;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>

