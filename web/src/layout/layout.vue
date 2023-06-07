<template>
  <div class="frame">
    <!-- 菜单 -->
    <div class="menu">
      <menu-win ref="menu" />
    </div>
    <div style="width: 1px; height: 100%; background-color: #cdccd7"></div>

    <!-- 主体 -->
    <div class="main">
      <!-- 头部导航条 -->
      <bar />

      <div class="body">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>


<script>
import menuWin from "./components/menu/menu.vue";
import bar from "./components/bar/bar.vue";
export default {
  name: "frame",
  components: {
    menuWin,
    bar
  },
  data() {
    return {};
  },
  methods: {},

  created() {
    //获取页面数据
    this.$store.dispatch("page/note/fetchPageList").then(() => {
      //首次打开页面
      this.$refs.menu.openFirstPage();
    });

  },


};
</script>

<style scoped>
.frame {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  display: flex;
}

.menu {
  width: 284px;
  /**全系统这里要修正，另外main的width会影响这里的实际值，目前的方案是 .main---width: calc(100% - 300px);*/
  min-width: 143px;
  height: 100%;
  background-color: #F0F0F3;
}

.main {
  width: calc(100% - 285px);
  height: 100%;
  /*总宽度100%-menu宽度284px-分隔线宽度1px;*/
}

.body {
  width: 100%;
  height: calc(100% - 40px);
  overflow-y: auto;

}




</style>