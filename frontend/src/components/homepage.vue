<template>
  <div id="homepage">
    <div id="settingBar">
      <div id="urlBox">
        目前支持搜索的网址
        <div v-for="url in urlList" :key="url">
          {{ url }}
        </div>
      </div>
      <div id="keywordsBox">
        <div id="addKeywordBar">
          <input v-model="keyword" placeholder="输入关键词">
          <button id='addKeywordButton' @click="addKeyword">添加关键词</button>
        </div>
        <div id="keywordsContainer">
          <div class="keywordContainer" v-for="word in keywordsList" :key="word">
            <div>{{ word }}</div>
            <div class="delKeywordButton" @click="delKeyword" :id="word">×</div>
          </div>
        </div>
      </div>
      <button id="searchButton"
           :disabled="isDisabled"
           @click="search">{{ searchButtonText }}</button>
    </div>
    <div id="articleBox">
      <div v-for="article in articleList" :key="article.id">
        <a :href="article.url">{{ article.title }}</a>
      </div>
    </div>
  </div>
</template>

<script>
import reptileAPI from '@/api/reptileAPI'

export default {
  name: 'homepage',
  data () {
    return {
      keyword: '',
      keywordsList: [],
      urlList: ['http://gzdaily.dayoo.com'],
      articleList: [],
      taskList: [],
      intervalId: '',
      isDisabled: false,
      searchButtonText: '搜索'
    }
  },
  computed: {
  },
  methods: {
    addKeyword (event) {
      if (!this.keywordsList.includes(this.keyword)) {
        this.keywordsList.push(this.keyword)
      }
    },
    delKeyword (event) {
      var word = event.currentTarget.id
      this.keywordsList = this.keywordsList.filter(e => {
        return e !== word
      })
    },
    search (event) {
      if (this.keywordsList.length === 0) {
        alert('请输入关键字')
        return
      }

      this.taskList = []
      this.articleList = []

      reptileAPI.gzdaily(this.keywordsList, response => {
        if (response.status === 200) {
          this.taskList.push(response.data.task)
        } else {
          alert('gzdaily status code error')
        }
      }, response => {
        alert('gzdaily request error')
      })

      reptileAPI.huxiu(this.keywordsList, response => {
        if (response.status === 200) {
          this.taskList.push(response.data.task)
        } else {
          alert('huxiu status code error')
        }
      }, response => {
        alert('huxiu request error')
      })

      this.searchButtonText = '搜索中'
      this.isDisabled = true
    }
  },
  created () {
    this.intervalId = setInterval(() => {
      if (this.taskList.length !== 0) {
        reptileAPI.getResults(this.taskList, response => {
          var results = response.data.data

          results.forEach(e => {
            // 上一次的请求可能在两秒之内都没有response，但实际上已经完成了
            // 这样就会对同一个已完成的taskId发送多次查询
            // article会添加两次
            // 这里的isResponseArrived用于解决这个问题
            // console.log(e.id)
            console.log(this.taskList.includes(e.id))
            var isResponseArrived = true
            this.taskList.forEach(task => {
              if (task.id === e.id) {
                isResponseArrived = false
              }
            })

            if (!isResponseArrived) {
              this.articleList = this.articleList.concat(e.results)
              this.taskList = this.taskList.filter(task => {
                if (task.id !== e.id) {
                  return task
                }
              })
            }
          })

          if (this.taskList.length === 0) {
            this.isDisabled = false
            this.searchButtonText = '搜索'
          }
        }, response => {
          alert('Get Results Error')
        })
      }
    }, 3000)
  },
  beforeDestroy () {
    clearInterval(this.intervalId)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

#homepage {
  position: relative;
  display: flex;
}

#settingBar {
  position: relative;
  float: left;
  width: 300px;
  margin-left: 50px;
}

#urlBox {
  /* position: absolute;
  left: 50px; */
  width: 100%;
  margin: 0 0 50px 0;
}

#keywordsBox {
  /* position: absolute;
  left: 50px;
  top: 300px; */
  width: 100%;
  margin: 0 0 50px 0;
}

#addKeywordBar {
  display: flex;
}

/* input {
  padding: 3px 5px 3px 5px;
  border-radius: 0%;
  border: none;
  background-color: #7f8183;
  opacity: 0.7;
  border-color: #6c757d;
  color: black;
  margin: 0;
} */

#addKeywordButton {
  width: 85px;
  margin: 0 0 0 0;
}

#searchButton {
  cursor: pointer;
  width: 30%;
  margin: 0 auto 0 auto;
  padding: 3px 5px 3px 5px;
}

.button {
  /* position: absolute; */
  user-select: none;
  padding: 3px 5px 3px 5px;
  background-color: cadetblue;
  box-shadow: rgba(0, 0, 0, 0.117647) 1px 2px 6px, rgba(0, 0, 0, 0.117647) 1px 2px 6px;
  transition: .15s all ease-in-out;
}

.button:hover {
  /* position: absolute; */
  cursor: pointer;
  transform: scale(1.1);
}

.button:active {
  transform: scale(0.95);
}

#keywordsContainer {
    position: relative;
    display: flex;
}

.keywordContainer {
  user-select:none;
  position: relative;
  display: flex;
  width: auto;
  padding: 3px 5px 3px 5px;
  margin: 3px 5px 3px 5px;
  background-color: bisque;
}

.delKeywordButton {
  width: 12px;
  margin: 0;
  top: 0;
  right: 0;
  padding-top: 2px;
  color: black;
}

.delKeywordButton:hover {
  cursor: pointer;
  color: white;
}

/*right part*/
#articleBox {
  margin: 0 auto 0 auto;
}

::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
    color: black;
    opacity: 1; /* Firefox */
}

</style>
