<template>
  <div
    id="aiBoard"
    class="aiboard-container"
    v-show="isShow.visible"
    @click="closeSelf()"
  >
    <div
      class="ai-plus"
      v-show="isShowAIPlus"
      @click.stop
      :style="{
        top: plus_pos.top + 'px',
        left: plus_pos.left + 'px',
      }"
    >
      <div class="plus-item" @click="selectPlus('image_gen')">
        <div class="plus-icon"><i class="fa-regular fa-image"></i></div>
        <div class="plus-name">#图像生成</div>
      </div>
      <div class="plus-item" @click="selectPlus('knowledge')">
        <div class="plus-icon"><i class="fa-solid fa-book"></i></div>
        <div class="plus-name">#知识库问答</div>
      </div>
    </div>

    <div
      class="input-pack"
      @click.stop
      :style="{
        top: input_pos.top + 'px',
        left: input_pos.left + 'px',
        width: input_pos.width + 'px',
      }"
    >
      <i class="input-icon fa-solid fa-wand-magic-sparkles"></i>
      <div
        class="my-input"
        ref="aiinput"
        contenteditable="true"
        @input="checkInput($event)"
        type="text"
        v-html="inputData"
        placeholder="向AI输入消息"
      ></div>
      <div class="send-icon-pack">
      <i class="send-icon fa-regular fa-paper-plane"></i>
    </div>
    </div>

    <div
      class="item-pack"
      @click.stop
      :style="{
        top: select_pos.top + 'px',
        left: select_pos.left + 'px',
      }"
    >
      <div class="item-handle" v-for="aiItem in aiHandle">
        <div class="item-part">
          <div class="item-icon" :class="aiItem.icon"></div>
          <div>{{ aiItem.name }}</div>
        </div>
        <div class="item-last-icon">
          <i class="fa-solid fa-arrow-turn-down"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "aiBoard",
  data() {
    return {
      inputData: "",
      isShowAIPlus: false,
      plusData: null,
      aiHandle: [
        {
          name: "翻译",
          icon: "fa-solid fa-language",
          type: "translate",
          path: "",
        },
        {
          name: "摘要",
          icon: "fa-regular fa-paste",
          type: "summary",
          path: "",
        },
        {
          name: "会议纪要",
          icon: "fa-regular fa-pen-to-square",
          type: "meeting",
          path: "",
        },
        {
          name: "周报",
          icon: "fa-regular fa-file-lines",
          type: "weekly",
          path: "",
        },
        {
          name: "续写",
          icon: "fa-solid fa-diagram-project",
          type: "continue",
          path: "",
        },
      ],
    };
  },
  computed: {
    isShow() {
      return this.$store.state.page.note.isShowAiBoard;
    },
    aiData() {
      return this.$store.state.page.note.aiData;
    },

    //输入框位置
    input_pos() {
      if (this.aiData.targetRect == null) {
        return {
          top: 0,
          left: 0,
          width: 0,
        };
      }
      let top = this.aiData.targetRect.top;
      let left = this.aiData.targetRect.left;
      let width = this.aiData.targetRect.width;
      return {
        top: top,
        left: left,
        width: width,
      };
    },
    //ai快捷选项位置
    select_pos() {
      let top = this.input_pos.top + 43;
      let left = this.input_pos.left;
      return {
        top: top,
        left: left,
      };
    },

    // ai增强选项的位置
    plus_pos() {
      let top = this.input_pos.top - 118;
      let left = this.input_pos.left + 30;
      return {
        top: top,
        left: left,
      };
    },
  },
  watch: {},

  methods: {
    //关闭弹框
    closeSelf() {
      this.$store.commit("page/note/setIsShowAiBoard", "close_all");
    },

    //选择ai增强类型
    selectPlus(type) {
      this.plusData = type;
      if (type == "image_gen") {
        this.inputData =
          "<span style='color:#4262FF; margin-right:2px'>#图像生成</span><span > &nbsp </span>";
      }

      if (type == "knowledge") {
        this.inputData =
          "<span style='color:#4262FF; margin-right:2px'>#知识库问答</span><span > &nbsp </span>";
      }
    },

    checkInput(e) {
      console.log("this.inputData123", e.target.innerHTML);
      let val = e.target.innerHTML;
      //当输入框为空时，关闭ai扩展类型 Plus；当输入框不为空时，且首位是#加上其他字符时，关闭ai扩展类型 Plus
      if (val == "" || val != "#") {
        this.isShowAIPlus = false;
      }
      if (val == "#") {
        this.isShowAIPlus = true;
      }
    },
  },
};
</script>

<style scoped>
.aiboard-container {
  width: 100%;
  height: 100vh;

  z-index: 99;
  position: fixed;
  top: 0px;
  left: 0px;
}

.ai-plus {
  width: 320px;
  height: 112px;
  position: fixed;
  border-radius: 6px;
  padding: 0px 6px;
  box-sizing: border-box;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  overflow: auto;
  z-index: 100;
  background-color: #fff;
  border: 1px solid #ccc;
  box-shadow: 0 1px 6px #ccc;
}

.plus-item {
  width: 100%;
  height: 40px;
  margin-top: 6px;
  border-radius: 6px;
  padding: 0px 12px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  cursor: pointer;
}

.plus-item:hover {
  background-color: #eee;
}
.plus-name {
  color: #4262ff;
  margin-left: 8px;
}

.input-pack {
  width: 100%;
  height: 40px;
  border-radius: 6px;
  overflow: hidden;
  display: flex;

  align-items: center;
  background-color: #fff;
  border: 1px solid #ccc;
  box-shadow: 0 1px 6px #ccc;
  position: fixed;
  top: 0px;
  left: 0px;
  z-index: 100;
}

.input-icon{
  width: 36px;
  height: 36px;
  line-height: 36px;
  text-align: center;
  font-size: 20px;
  color: #6956e8;
}
.send-icon-pack{
  width: 42px;
  height: 32px;
  border-radius: 6px;
  line-height: 32px;
  text-align: center;
  font-size: 18px;
  margin-right: 6px;
  color: #707070;
  cursor: pointer;
}
.send-icon-pack:hover{
  color: #000;
  background-color: #c0bbf3;

}
.my-input {
  width: calc(100% - 36px);
  height: 40px;
  line-height: 40px;
  text-align: left;
  box-sizing: border-box;
  font-size: 16px;
  border: none;
  outline: none;
  background-color: #fff;
}

.item-pack {
  width: 450px;
  position: fixed;
  margin-top: 6px;
  border-radius: 6px;
  padding: 16px 6px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: auto;
  z-index: 100;
  background-color: #fff;
  border: 1px solid #ccc;
  box-shadow: 0 1px 6px #ccc;
}

.item-handle {
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

.item-last-icon {
  height: 40px;
  line-height: 40px;
  transform: rotate(90deg);
  color: #a6a6a6;
  visibility: hidden;
}
.item-handle:hover .item-last-icon {
  visibility: visible;
}
</style>