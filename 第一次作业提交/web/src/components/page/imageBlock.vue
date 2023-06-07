
<template>
  <div class="image-viewer" ref="imageViewer">

    <div
      v-show="text"
      class="image-pack"
      :style="{ width: imageSize.width + 'px' }"
      ref="imagePack"
    >
      <div class="image-inner">
        <img ref="image" class="image" :src="'http://127.0.0.1:8000/'+text" />
        <div
          class="resize-handle left"
          @mousedown="resizeStart($event, 'left')"
          ref="leftHandle"
        >
          <div class="tag-resize"></div>
        </div>
        <div
          class="resize-handle right"
          @mousedown="resizeStart($event, 'right')"
          ref="rightHandle"
        >
          <div class="tag-resize"></div>
        </div>
        <div class="menu">
          <div class="menu-item fa-regular fa-comment-dots"></div>
          <div class="menu-item align">
            <div><i class="fa-solid fa-align-center"></i></div>
            <div class="align-buttons">
              <div class="align-btn" @click="alignLeft">
                <i class="fa-solid fa-align-left"></i>
              </div>
              <div class="align-btn" @click="alignCenter">
                <i class="fa-solid fa-align-center"></i>
              </div>
              <div class="align-btn" @click="alignRight">
                <i class="fa-solid fa-align-right"></i>
              </div>
            </div>
          </div>
          <div class="menu-item fa-regular fa-pen-to-square"></div>
          <div class="menu-item fa-solid fa-download"></div>
          <div class="menu-item fa-solid fa-ellipsis"></div>
        </div>
      </div>
    </div>

    <el-upload
      :show-file-list="false"
      :http-request="uploadImage"
      action=""
    >
      <div class="image-upload" v-show="!text">
        <div class="image-upload-icon"><i class="fa-regular fa-image"></i></div>
        <div>上传图像</div>
      </div>
    </el-upload>

  </div>
</template>

<script>
import * as api from "@/views/page/api.js";


export default {
  name: "imageBlock",
  props: {
    blockData: {
      type: Object,
      default: () => {
        return {
          id: null,
          type: "image",
          data: {
            text: "",
          },
        };
      },
    },
    text: {
      type: String,
      default: ""
    },

    imageWidth: {
      type: Object,
      default: () => {
        return {
          imageSize: { width: 300 },
        };
      },
    },
  },
  data() {
    return {
      imagePath: this.text,
      imageSize: this.imageWidth.imageSize,
      explain: "", //暂时不用，图像说明
      alignItems: "center",

      originalImageSize: null,
      resizeDirection: null,
      resizeStartX: null,
    };
  },

  computed:{
    now_page_id() {
      return this.$store.state.page.note.now_page_id
    },
  },


  watch: {
    alignItems() {
      this.$refs.imageViewer.style.alignItems = this.alignItems;
    },
  },
  methods: {
    alignLeft() {
      this.alignItems = "flex-start";
    },
    alignCenter() {
      this.alignItems = "center";
    },
    alignRight() {
      this.alignItems = "flex-end";
    },

    resizeStart(event, direction) {
      this.originalImageSize = { ...this.imageSize };
      this.resizeDirection = direction;
      this.resizeStartX = event.clientX;
      window.addEventListener("mousemove", this.resize);
      window.addEventListener("mouseup", this.resizeEnd);
    },
    resize(event) {
      if (this.resizeDirection === "left") {
        this.imageSize.width =
          this.originalImageSize.width + (this.resizeStartX - event.clientX);
        if (this.imageSize.width < 60) {
          this.imageSize.width = 60;
        }
      } else if (this.resizeDirection === "right") {
        this.imageSize.width =
          this.originalImageSize.width - (this.resizeStartX - event.clientX);
        if (this.imageSize.width < 60) {
          this.imageSize.width = 60;
        }
      }
    },
    resizeEnd() {
      window.removeEventListener("mousemove", this.resize);
      window.removeEventListener("mouseup", this.resizeEnd);
    },




    //上传图片
    uploadImage(file) {
      let formData = new FormData()
      formData.append('pic', file.file)
      formData.append('block_id', this.blockData.id)

      api. UPLOAD_IMAGE(formData).then((res) => {
        this.$message.success('上传成功')
        this.$store.dispatch("page/note/fetchPageDetail", this.now_page_id)
      }).catch((e) => {
        this.$message.error(e.message)
      })
    },





  },
  mounted() {
    this.originalImageSize = { ...this.imageSize };
  },
};
</script>


<style scoped>
.image-viewer {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.image-pack {
  max-width: 100%;
}

.image-inner {
  width: 100%;
  position: relative;
}

.image {
  width: 100%;
  height: 100%;
}

.resize-handle {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 10px;
  cursor: col-resize;
  display: flex;
  justify-content: center;
  align-items: center;
}

.left {
  left: 0;
}

.right {
  right: 0;
}

.tag-resize {
  width: 6px;
  height: 60px;
  border: 1px solid #fff;
  border-radius: 3px;
  visibility: hidden;
}

.image-pack:hover .tag-resize {
  visibility: visible;
}

.menu {
  display: flex;
  align-items: center;
  background-color: #000;
  color: #fff;
  position: absolute;
  top: 4px;
  right: 4px;
  border-radius: 4px;
  visibility: hidden;
}

.image-pack:hover .menu {
  visibility: visible;
}

.menu-item {
  padding: 0 14px;
  height: 30px;
  line-height: 30px;
  cursor: pointer;
  border-right: 1px solid #a6a6a6;
}

.menu-item:hover {
  background-color: #252424;
}

.menu-item:first-child {
  border-radius: 4px 0 0 4px;
}

.menu-item:last-child {
  border-right: none;
  border-radius: 0 4px 4px 0;
}

.align {
  position: relative;
}

.align-buttons {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  justify-content: center;
  margin-top: 10px;
  border-radius: 4px;
  visibility: hidden;
  padding-top: 6px;
}

.align:hover .align-buttons {
  visibility: visible;
}

.align-btn {
  padding: 0 12px;
  height: 30px;
  line-height: 30px;
  border-right: 1px solid #a6a6a6;
  background-color: #000;
  color: #fff;
}

.align-btn:hover {
  background-color: #252424;
}

.align-btn:first-child {
  border-radius: 4px 0 0 4px;
}

.align-btn:last-child {
  border-right: none;
  border-radius: 0 4px 4px 0;
}

.image-upload {
  width: 100%;
  height: 50px;
  border-radius: 6px;
  padding: 0 16px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  background-color: #e4e4e4;
  color: #707070;
}
.image-upload-icon {
  font-size: 20px;
  margin-right: 10px;
}
</style>


