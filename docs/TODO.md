# TODO: 内存化后续测试流程

## 测试顺序
- [ ] 先测试基础组件：`restaurant_detector`、`element_detector`、`menu_detector`
- [ ] 再测试工作流：`workflow_manager`
- [ ] 组件测试通过后，再做工作流联调验证

## 测试关注点
- [ ] 确认截图、OCR、LLM 输入均可在内存中流转
- [ ] 确认不再生成历史中间图片和中间 JSON
- [ ] 确认最终输出 `restaurants.json` 内容正确

## 说明
- [ ] 暂不执行测试，留待后续人工验证
- [ ] 如测试暴露问题，优先回到对应组件修复，再重新跑工作流