<template>
  <div class="blockmenu-container" v-show="isShow" @click="closeSelf()">
    <div class="menu-body" :style="{
      top: position.top + 'px',
      left: position.left + 'px',
    }">


<div class="item-handle">
        <div class="item-part">
          <div class="item-icon fa-solid fa-wand-magic-sparkles"></div>
          <div>向AI提问</div>
        </div>
        <div class="item-last-icon"><i class="fa-solid fa-arrow-turn-down" ></i></div>
      </div>


      <div class="item-handle ai-handle">
        <div class="item-part">
          <div class="item-icon fa-regular fa-image"></div>
          <div>AI操作</div>
        </div>
        <div class="item-go-icon"><i class="fa-solid fa-angle-right"></i></div>


<div class="ai-handle-menu">

        <div class="ai-handle-item" v-for="aiItem in aiItemData">
        <div class="item-part">
          <div class="item-icon" :class="aiItem.icon"></div>
          <div>{{ aiItem.name }}</div>
        </div>
        <div class="ai-last-icon"><i class="fa-solid fa-arrow-turn-down" ></i></div>
      </div>
    </div>


      </div>

      <div class="item-handle" v-for="item in itemData" @click="selectHandle(item)">
        <div class="item-part">
          <div class="item-icon" :class="item.icon"></div>
          <div>{{ item.name }}</div>
        </div>
        <div class="item-last-icon"><i class="fa-solid fa-arrow-turn-down" ></i></div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'blockMenu',
  data() {
    return {
      itemData:[
        {name:"知识库问答", icon:"fa-solid fa-book", type:"knowledge", shortcut:""},   
        {name:"图像生成", icon:"fa-regular fa-image", type:"pic_gen", shortcut:""},
        {name:"删除", icon:"fa-regular fa-trash-can", type:"del", shortcut:""},
        {name:"复制", icon:"fa-solid fa-clone", type:"", shortcut:""},
      ],

      aiItemData:[
     
        {name:"翻译", icon:"fa-solid fa-language", type:"translate", path:""},
        {name:"摘要", icon:"fa-regular fa-paste", type:"summary", path:""},
        {name:"会议纪要", icon:"fa-regular fa-pen-to-square", type:"meeting", path:""},
        {name:"周报", icon:"fa-regular fa-file-lines", type:"weekly", path:""},
        {name:"续写", icon:"fa-solid fa-diagram-project", type:"continue", path:""},
      ],

    }
  },
  computed: {

    now_block_id(){
      return this.$store.state.page.note.now_block_id
    },


    isShow() {
      console.log("blockMenuData.visible", this.$store.state.page.note.blockMenuData.visible)
      return this.$store.state.page.note.blockMenuData.visible
    },

    position(){
      let targetRect = this.$store.state.page.note.blockMenuData.targetRect
      if(targetRect == null){
        return {
          top: 0,
          left: 0,
        }
      }
      let left = targetRect.left - 326;

      //若顶部超出屏幕
      let top = targetRect.top - 150;
      if(top < 0){
        top = 6;
      }
      
      //获取屏幕高度
      let screenHeight = document.documentElement.clientHeight;
      //若底部超出屏幕
      if(top + 420 > screenHeight){
        top = screenHeight - 426;
      }

      return {
        top: top,
        left: left,
      }
    },

  },

  methods: {

    closeSelf(){
      let data = {
        visible: false,
        targetRect: null,
      }
      this.$store.commit('page/note/setBlockMenuData', data)
    },

    //菜单操作
    selectHandle(item){
      if(item.type=="del"){
        this.$store.dispatch('page/note/fetchDeleteBlock', this.now_block_id)
      }
    }

  }

}
</script>

<style scoped>
.blockmenu-container{
  width: 100%;
  height: 100vh;
  
  z-index: 99;
  position: fixed;
  top: 0px;
  left: 0px;
}


.menu-body{
  width: 320px;
  height: 300px;
  border-radius: 6px;
  position: fixed;
  padding: 0px 6px;
  box-sizing: border-box;
  z-index: 100;
  background-color: #fff;
  border: 1px solid #ccc;
  box-shadow: 0 1px 6px #ccc;
  padding-top: 6px;
}

.item-handle, .ai-handle-item {
  width: 100%;
  height: 40px;
  margin-top: 6px;
  border-radius: 6px;
  padding: 0px 12px;
  box-sizing: border-box;
  display: flex;
  justify-content: space-between;
  cursor: pointer;
}
.item-handle:hover {
  background-color: #eee;
}

.item-part {
  display: flex;
  align-items: center;
}

.item-icon {
  margin-right: 8px;
}
.item-go-icon{
  height: 40px;
  line-height: 40px;
}
.item-last-icon {
  height: 40px;
  line-height: 40px;
  transform: rotate(90deg);
  color:#A6A6A6;
  visibility: hidden;
}
.item-handle:hover .item-last-icon {
  visibility: visible;
}


.ai-handle{
  position: relative;
}
.ai-handle-menu{
  position: absolute;
  top: -60px;
  right: -284px;
  width: 280px;
  height: 240px;
  border-radius: 6px;
  padding: 0px 6px;
  box-sizing: border-box;
  z-index: 300;
  background-color: #fff;
  border: 1px solid #ccc;
  box-shadow: 0 1px 6px #ccc;
  visibility: hidden;
}
.ai-handle:hover .ai-handle-menu{
  visibility: visible;
}
.ai-handle-item:hover {
  background-color: #eee;
}
.ai-last-icon{
  height: 40px;
  line-height: 40px;
  transform: rotate(90deg);
  color:#A6A6A6;
  visibility: hidden;
}

.ai-handle-item:hover .ai-last-icon{
  visibility: visible;
}


</style>