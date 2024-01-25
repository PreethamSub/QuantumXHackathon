<template>
  <main>
    <div class="container">
      <h1 style="color: rgb(134, 46, 216);" class="text-center">Blog generator</h1>

      <!-- displaying the blog -->
      <div id="blog-content">
        <div v-for="blogValue in blogContent" v-id="blogValue.id">
          <div class="heading" v-if="blogValue.type == 'HEADING'"><h2>{{ blogValue.content }}</h2></div>
          <div class="text" v-if="blogValue.type == 'TEXT'">{{ blogValue.content }}</div>
          <div class="image text-center" v-if="blogValue.type == 'IMAGE'"><img v-bind:src=blogValue.url></div>
        </div>
      </div>
      <div id="prompt" class="text-center">
        <!-- <span>Enter your prompt:</span> -->
        <input type="text" v-model="prompt">
        <button @click="callAPI()">Go</button>
      </div>
      
    </div>
    
  </main>
</template>

<script>
  import axios from "axios";
  export default {
    data(){
      return{
        prompt : "  Enter prompt here",
        heading :"  Enter heading",
        blogContent : [
          {id : 3 , type : "HEADING" , content : "Content"},
          {id : 1 , type : "TEXT" , content : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."},
          {id : 2 , type : "IMAGE" , url : "https://source.unsplash.com/random/300x300"},
        ]
      }
    },
    methods:{
      callAPI : async function(){
        let response = await axios.post("http://172.21.21.170:5000/generate" , {prompt : this.prompt});
        console.log(response)
        this.blogContent[1].content = response.data[0].summary_text
      }
    }
  };
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;500;600&display=swap');

  *{
    font-family: 'Poppins', sans-serif;
  }
  /* #container{
    margin-left: 5vw;
    margin-right: 5vw;
  } */

  .text-center{
    text-align: center;
  }

  input{
    height: 5vh;
    background-color: #F1F1F1;
    border: 1px solid #656565;
    color: #656565;
    border-radius: 10px;
    width: 70vw;
    margin: 1vw;
    box-shadow:2px 2px 0 0 #aeaeae;
    background: #fff;
  }

  .input_small{
    width: 25vw;
  }
  button{
    color: white;
    background-color: rgb(134, 46, 216);
    padding: 1.3vh 2vw;
    border: none;
    border-radius: 10px;
  }
  img{
    margin: 3vh;
  }

  h2{
    margin: 0 0;
  }
</style>
