<template>
    <div id="receiver">
        <h1>{{ title }}</h1>
        <ul>
            <li v-for="post in posts" :key="post.id">
                <p><strong>{{ post.title }}</strong></p>
                <p>{{ post.body }}</p>
            </li>
        </ul>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'Receiver',
        props: {
            title: String
        },
        data() {
            return {
                posts: []
            }
        },
        created() {
            axios.get('https://jsonplaceholder.typicode.com/posts')
                .then(response => {
                    this.posts = response.data;
                })
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    h3 {
        margin: 40px 0 0;
    }

    ul {
        list-style-type: none;
        padding: 0;
    }

    li {
        display: inline-block;
        margin: 0 10px;
    }

    a {
        color: #42b983;
    }
</style>
