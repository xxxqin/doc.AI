<template>
  <div class="bar-container">
    <div class="bar-left">
      <div class="bar-arrows">
        <el-tooltip effect="dark" content="显示菜单" placement="bottom">
          <div
            class="iconfont ykg-xiangyou display-icon"
            @click="showMenuHandle()"
            v-show="!isShowDisplayMenu"
          ></div>
        </el-tooltip>
        <el-tooltip effect="dark" content="返回项目" placement="bottom">
          <div
            class="iconfont ykg-zhuye display-icon"
            @click="goHome()"
            v-show="!isShowDisplayMenu"
          ></div>
        </el-tooltip>

        <el-tooltip effect="dark" content="后退" placement="bottom">
          <div class="back-icon" @click="goback()"><i class="fa-solid fa-chevron-left"></i></div>
        </el-tooltip>
        <el-tooltip effect="dark" content="前进" placement="bottom">
          <div
            class="forward-icon"
            @click="goForward()"
          ><i class="fa-solid fa-chevron-right"></i>
        </div>
        </el-tooltip>
      </div>


      <div class="bar-title-container">
        <div class="bar-title-pack">
          <span class="bar-title" @click="goPage()">{{ pageData.title?pageData.title:"未命名" }}</span>
        </div>
      </div>
    </div>

    <div class="right">

      <div class="item-icon" @click="openComment()"><i class="fa-regular fa-comment-dots"></i></div>
      <div class="item-icon"><i class="fa-regular fa-star"></i></div>
      


    </div>
  </div>
</template>

<script>
export default {
  name: "bar",
  data() {
    return {
      isShowDisplayMenu: true,
    };
  },
  computed: {
    // 获取块菜单数据
    pageData() {
      return this.$store.getters["page/note/getNowPageData"];
    },
  },

  methods: {
    //打开用户弹窗

    //打开评论弹窗
    openComment(){
      this.$store.commit("space/space/setIsShowRightWin", true);
    },




    
  },
};
</script>

<style scoped>
.bar-container {
  width: 100%;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.bar-left {
  display: flex;
  align-items: center;
}
.bar-arrows {
  display: flex;
  align-items: center;
  margin-left: 6px;
}

.display-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin-left: 6px;
  height: 30px;
  width: 30px;
  cursor: pointer;
  font-weight: bold;
}

.display-icon:hover {
  background-color: #e4e4e4;
  border-radius: 4px;
  color: #050038;
}

.back-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin-left: 6px;
  height: 30px;
  width: 30px;
  cursor: pointer;
}
.back-icon:hover {
  background-color: #e4e4e4;
  border-radius: 4px;
  color: #050038;
}
.forward-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin-left: 6px;
  height: 30px;
  width: 30px;
  color: #cecece;
}
.showforwardicon {
  cursor: pointer;
  color: #707070;
}
.showforwardicon:hover {
  background-color: #e4e4e4;
  border-radius: 4px;
  color: #050038;
}

.bar-title-container {
  display: flex;
  align-items: center;
  margin-left: 2px;
}

.bar-title {
  display: inline-block;
  height: 30px;
  line-height: 30px;
  padding: 0px 5px;
  border-radius: 4px;
  cursor: pointer;
}

.bar-title:hover {
  color: #050038;
  background-color: #e4e4e4;
}

.bar-title-division {
  margin: 0 3px;
  font-size: 18px;
  display: inline-block;
  transform: rotate(12deg);
}

.right {
  display: flex;
  align-items: center;
}

.item-icon {
  width: 30px;
  height: 30px;
  border-radius: 4px;
  margin-right: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-icon:hover {
  background-color: #e4e4e4;
}

.ai-help {
  height: 26px;
  padding: 0 12px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  margin-right: 8px;
  cursor: pointer;
  border: 1px solid #707070;
}
.ai-help:hover {
  background-color: #e4e4e4;
}

.ai-help > i {
  font-size: 16px;
  margin-right: 6px;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  margin-right: 10px;
}
</style>