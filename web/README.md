# docai

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).




      <div
        class="text-container"
        :class="{'text-focus':firstFocus}"
        ref="text"
        contenteditable="true"
        @keydown.enter.prevent="addItem"
        @keyup="handleKeyDown"
        @mouseup="handleMouseUp"
        v-html="data.text"
        @focus="textFocus"
        @blur="textBlur"
      ></div>

     @keydown="handleKeyDown"首字符有问题
          @keyup="handleKeyDown"这样改才行

