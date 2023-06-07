<template>
  <div 
    id="selectBoard" 
    class="select-body"
    :style="{
      top: position.top + 'px',
      left: position.left + 'px',
    }" 
    v-show="isShow.visible"
  >
    <div class="select-item" v-for="(option, index) in filteredOptions" :key="index" @click="selectOption(option.type)">
      <div class="item-icon" :class="option.icon">

      </div>
      <div class="item-status">
        <div>{{ option.name }}</div>
        <div class="item-explain">{{ option.text }}</div>        
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'selectBoard',
  data() {
    return {
      filteredOptions: [
        {
          name: '文本',
          icon: 'fa-solid fa-font',
          type: 'text',
          text:'用于进行文本的编辑'
        },
        {
          name: '标题',
          icon: 'fa-solid fa-heading',
          type: 'head',
          text:'用于作为标题'
        },
        {
          name: '图像',
          icon: 'fa-regular fa-image',
          type: 'image',
          text:'图像的容器'
        },
      ],
    }
  },
  computed: {
    now_page_id() {
      return this.$store.state.page.note.now_page_id
    },
    now_block_id() {
      return this.$store.state.page.note.now_block_id
    },


    isShow() {
      return this.$store.state.page.note.isShowSelBoard
    },
    boardData() {
      return this.$store.state.page.note.selectBoardData
    },
    position(){
      let top = this.boardData.top;
      let left = this.boardData.left;
      //获取屏幕宽度和高度
      let screenWidth = document.documentElement.clientWidth;
      let screenHeight = document.documentElement.clientHeight;
      if (top + 360 > screenHeight) {
        top = screenHeight - 388;
      }
      if (left + 440 > screenWidth) {
        left = screenWidth - 450;
      }

      return {
        top: top,
        left: left,
      }
    }

  },
  watch: {

    'isShow.visible': {
      handler(val) {
        if (val) {
          document.addEventListener('click', this.closeBoard)
        } else {
          document.removeEventListener('click', this.closeBoard)
        }
      },
      deep: true
    }

  },

  methods: {

    //点击弹框外部关闭弹框
    closeBoard() {
      let board = document.getElementById("selectBoard");
      if (board) {
        if (!board.contains(event.target)) {
          if (this.isShow.visibleIng) {
            this.$store.commit('page/note/setIsShowSelBoard', "close_all")
          } else {
            this.$store.commit('page/note/setIsShowSelBoard', "close_last")
          }
        }
      }

    },


    //选择一个选项
    selectOption(type) {
      let data = {
        target_id:this.now_block_id,
        page_id:this.now_page_id,
        type: type,
        data: {text:""}
      }


      this.$store.dispatch('page/note/fetchAddBlock',data)
      this.$store.commit('page/note/setIsShowSelBoard', "close_all")
    
    },

  }

}
</script>

<style scoped>
.select-body {
  width: 400px;
  padding: 16px 0px;
  position: fixed;
  top: 0px;
  left: 250px;
  border-radius: 8px;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
  border: 1px solid #ccc;
  box-shadow: 0 0 6px #ccc;
}

.select-item {
  width: 380px;
  height: 60px;
  text-align: center;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 0 10px;
  box-sizing: border-box;
  border-radius: 8px;
}

.select-item:hover {
  background-color: #dfdfe6;
}

.item-icon{
  width: 40px;
  height: 50px;
  font-size: 22px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
.item-status{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
}
.item-explain{
  font-size: 14px;
  color: #707070;
  margin-top: 4px;
}

</style>