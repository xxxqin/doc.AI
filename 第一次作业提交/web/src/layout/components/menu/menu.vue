<template>
  <div class="menu-container">
    <div class="menu-top">Doc.AI</div>
    <div class="menu-pack">
      <div class="item-pack" v-for="(item, index) in menuItem" :key="index" @click="selectItem(item, index)">
        <div class="item" >
          <div><i :class="item.icon"></i></div>
          <div class="item-name">{{ item.name }}</div>
        </div>
      </div>
    </div>
    <div class="page-menu">
      <div v-for="(menu, index) in menuData">
        <div
          class="option-inner"
          @click="openPage(menu)"
          :style="selectedBgcolor == menu.id ? 'background-color: #CDCCD7;' : ''"
        >
          <div class="option-part">
            <div class="option-icon">
              <i class="fa-regular fa-file-lines"></i>
            </div>
            <div>{{ menu.title?menu.title:'未命名' }}</div>
          </div>

          <div class="option-part">
            <el-dropdown trigger="click" placement="bottom-start">
            <div class="option-handle">
              <i class="fa-solid fa-ellipsis"></i>
            </div>
            <el-dropdown-menu class="drop-pack" slot="dropdown">
              <el-dropdown-item class="drop-item" @click.native="delPage(menu.id)"
                ><i class="drop-icon fa-regular fa-trash-can"></i>删除</el-dropdown-item
              >
            </el-dropdown-menu>
          </el-dropdown>


          </div>
        </div>
      </div>
    </div>

    <div class="menu-bottom">
      <div class="bottom-pack">
        <div class="bottom-item" @click="openSetting()">
          <div><i class="fa-solid fa-shapes"></i></div>
          <div class="bottom-title">设置</div>
        </div>
      </div>
      <div class="bottom-division"></div>
      <div class="bottom-pack">
        <div class="bottom-item" @click="openRecycle()">
          <div><i class="fa-regular fa-trash-can"></i></div>
          <div class="bottom-title">回收站</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "base_menu",
  data() {
    return {
      menuItem: [
      { icon: "fa-solid fa-book", name: "知识库", type: "knowledge", path: "" },   
        { icon: "fa-regular fa-star", name: "收藏", type: "collect", path: "" },

        { icon: "fa-solid fa-plus", name: "新建", type: "add", path: "" },
      ],


      selectedBgcolor: 0, //控制选中的menu的选项显示背景色
    };
  },
  computed: {

    menuData() {
      return this.$store.state.page.note.pageList
    }


  },

  methods: {
    //选择菜单项
    selectItem(item, index) {
      if (item.type == "add") {
        let data = {
          title:''
        }

        this.$store.dispatch("page/note/fetchAddPage", data)
        return;
      }
      if (item.type == "knowledge") {
        this.$router.push('/knowledge')

        return;
      }
      //this.$router.push(item.path);
    },


    //打开页面
    openPage(menu){
      this.$store.commit("page/note/setNowPageId", menu.id)
      this.$store.dispatch("page/note/fetchPageDetail", menu.id)
      this.$router.push('/note')
      this.selectedBgcolor = menu.id
    },

    //首次打开页面，如果有页面，则打开第一个页面，如果没有页面，则新建一个页面
    openFirstPage(){
      if(this.menuData.length > 0){
        let menu = this.menuData[0]
        this.openPage(menu)
        console.log('menu',menu)
      }
      else{
        let data = {
          title:''
        }
        this.$store.dispatch("page/note/fetchAddPage", data).then(res=>{
          let menu = this.menuData[0]
          this.openPage(menu)          //这里有错，menu没有值
        })
      }


    },


    // 删除页面
    delPage(menuId){
      this.$store.dispatch("page/note/fetchDeletePage", menuId)
    },

  },


  created() {
    //刷新页面时，如果有页面，则打开第一个页面
    if(this.menuData.length > 0){
        let menu = this.menuData[0]
        this.openPage(menu)
        console.log('menu',menu)
      }
  },



};
</script>

<style scoped>
.menu-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.menu-top {
  width: 100%;
  height: 40px;
  font-size: 24px;
  font-weight: bold;
  display: flex;
  align-items: center;
  padding-left: 16px;
  box-sizing: border-box;
}

.menu-pack {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.item-pack {
  width: 100%;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
}

.item {
  width: 274px;
  height: 46px;
  line-height: 46px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  box-sizing: border-box;
  padding: 0px 12px;
  cursor: pointer;
}
.item:hover {
  background-color: #dedde8;
}
.item-name {
  margin-left: 8px;
}

.page-menu {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 284px;
}

.option-inner {
  width: 264px;
  height: 52px;
  line-height: 52px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-sizing: border-box;
  padding: 0 6px;
  cursor: pointer;
}

.option-inner:hover {
  background-color: #dedde8;
}

.option-part {
  display: flex;
  align-items: center;
}

.option-icon {
  margin-right: 4px;
  font-size: 18px;
  width: 26px;
  height: 26px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.option-icon:hover {
  background-color: #a9a7b3;
}

.option-handle {
  width: 22px;
  height: 22px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  visibility: hidden;
}
.option-inner:hover .option-handle {
  visibility: visible;
}
.option-handle:last-child {
  margin-left: 6px;
}

.option-handle:hover {
  background-color: #a9a7b3;
}
.drop-pack{
  padding:12px 6px;
}

.drop-item{
  width: 150px;
  text-align: left;
  border-radius: 4px;
}
.drop-item:hover{
  color:#050038;
  background-color: #DEDDE8;

}
.drop-icon{
  margin-right: 6px;
}
.menu-bottom {
  width: 100%;
  height: 40px;
  display: flex;
  align-items: center;
  border-top: 1px solid #cdccd7;
  box-sizing: border-box;
  position: absolute;
  bottom: 0px;
  left: 0px;
}
.bottom-pack {
  width: 50%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.bottom-item {
  padding: 0 26px;
  height: 30px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.bottom-item:hover {
  background-color: #dedde8;
}
.bottom-division {
  width: 1px;
  height: 30px;
  background-color: #cdccd7;
}

.bottom-title {
  margin-left: 8px;
}
</style>