<template>
  <div class="page-container">
    <!-- 页头部 -->
    <div class="pic-pack">
      <img class="pic" src="@/assets/images/莫奈1.jpeg" />
      <div class="pic-handle">
        <div class="pic-handle-icon">更换封面</div>
        <div class="pic-handle-icon">调整位置</div>
      </div>
    </div>
    <!-- 页主体 -->
    <div class="page-body">
      <div class="body-top">
        <div class="without-img" v-show="0"></div>
        <div class="top-handle">
          <div class="handle-icon"><i class="fa-regular fa-heart"></i>图标</div>
          <div class="handle-icon"><i class="fa-regular fa-image"></i>封面</div>
        </div>

        <input class="title" placeholder="输入标题" v-model="pageData.title" />
      </div>

      <div class="item" v-for="(block, index) in blocks" :key="index">
        <div class="tag" :style="'height:' + block.height + 'px'">
          <div class="item-icon fa-solid fa-plus" @click="addTextBlock(block)"></div>
          <div class="item-icon mover" @click="openBlockMenu($event, block)">
            <i class="fa-solid fa-grip-vertical"></i>
          </div>
        </div>

        <block class="block" v-if="block.type == 'head'||block.type == 'text'" :type="block.type" :id="block.id" :data="block.data"></block>
        <image-block v-if="block.type == 'image'" class="block" :blockData="block" :text="block.data.text"></image-block>
      </div>
    </div>

    <ai-board />
    <select-board />
    <block-menu />
  </div>
</template>

<script>
import block from "@/components/page/block.vue";
import imageBlock from "@/components/page/imageBlock.vue";
import aiBoard from "@/components/board/aiBoard.vue";
import selectBoard from "@/components/board/selectBoard.vue";
import blockMenu from "@/components/board/blockMenu.vue";

export default {
  name: "page",
  components: {
    block,
    imageBlock,
    aiBoard, //AI输入框
    selectBoard, //块选项板
    blockMenu, //块菜单
  },
  data() {
    return {
      title: "标题",
      OLD_blocks: [
        { id: "2", type: "head", data: { text: "标题" } },
        { id: "3", type: "text", data: { text: "我是文本块" } },
        {
          id: "3",
          type: "image",
          data: {
            text: "https://img0.baidu.com/it/u=155154702,1277334029&fm=253&fmt=auto&app=138&f=JPEG?w=615&h=500",
          },
        },
      ],
    };
  },

  computed: {
    // 获取块菜单数据
    pageData() {
      return this.$store.state.page.note.nowPageData;
    },

    blocks() {
      return this.$store.getters["page/note/getNowPageBlocks"];
    },

  },
  watch: {

  },


  methods: {
    openBlockMenu(e,block) {

      //保存当前块id
      this.$store.commit("page/note/setNowBlockId", block.id);

      // 获取目标元素的位置信息
      let targetRect = e.target.getBoundingClientRect();
      let data = {
        visible: true,
        targetRect: targetRect,
      };
      this.$store.commit("page/note/setBlockMenuData", data);
    },

    // 添加文本块
    addTextBlock(block) {
      let data = {
        target_id:block.id,
        page_id:this.pageData.id,
        type: "text",
        data: {text:""}
      }
      this.$store.dispatch('page/note/fetchAddBlock',data)
    },



  },
};
</script>

<style scoped>
.page-container {
  width: 100%;
  height: 100%;
}

.pic-pack {
  width: 100%;
  height: 280px;
  position: relative;
}

.pic {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.pic-handle {
  display: flex;
  position: absolute;
  bottom: 6px;
  right: 240px;
  height: 30px;
  line-height: 30px;
  background-color: #fff;
  border-radius: 4px;
  font-size: 14px;
  overflow: hidden;
  visibility: hidden;
}

.pic-pack:hover .pic-handle {
  visibility: visible;
}

.pic-handle-icon {
  padding: 0 12px;
  cursor: pointer;
}

.pic-handle-icon:hover {
  background-color: #dedde8;
}

.pic-handle-icon:last-child {
  border-left: 1px solid #9e9898;
}

.page-body {
  width: 100%;
  padding: 0 240px;
  box-sizing: border-box;
  box-sizing: border-box;
}

.body-top {
  width: 100%;
  padding-top: 8px;
  box-sizing: border-box;
  position: relative;
}

.without-img {
  width: 100%;
  height: 40px;
}

.top-handle {
  width: 100%;
  display: flex;
  align-items: center;
  padding-left: 56px;
  box-sizing: border-box;
  visibility: hidden;
}

.body-top:hover .top-handle {
  visibility: visible;
}

.handle-icon {
  padding: 0 6px;
  height: 28px;
  line-height: 28px;
  border-radius: 4px;
  margin-right: 8px;
  cursor: pointer;
}

.handle-icon:hover {
  background-color: #dedde8;
}

.handle-icon > i {
  margin-right: 6px;
}

.title {
  width: 100%;
  font-size: 42px;
  font-weight: bold;
  text-align: left;
  margin-top: 4px;
  margin-bottom: 30px;
  padding-left: 56px;
  box-sizing: border-box;
  border: none;
  outline: none;
}

.item {
  width: 100%;
  display: flex;
  align-items: flex-start;
  margin-bottom: 6px;
}

.tag {
  width: 56px;
  height: 30px;
  padding-right: 8px;
  box-sizing: border-box;
  display: flex;
  justify-content: space-between;
  align-items: center;
  visibility: hidden;
}

.item:hover .tag {
  visibility: visible;
}

.item-icon {
  height: 24px;
  line-height: 24px;
  padding: 0 4px;
  border-radius: 4px;
  cursor: pointer;
}

.item-icon:hover {
  background-color: #dedde8;
}

.mover {
  cursor: grab;
}

.block {
  width: calc(100% - 56px);
}


</style>