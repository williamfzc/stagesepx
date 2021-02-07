# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [v0.15.2](https://github.com/williamfzc/stagesepx/releases/tag/v0.15.2) - 2021-02-02

<small>[Compare with v0.15.1](https://github.com/williamfzc/stagesepx/compare/v0.15.1...v0.15.2)</small>

### Bug Fixes
- Wrong calc in crophook ([72d47df](https://github.com/williamfzc/stagesepx/commit/72d47df5df0d3a54a80f8f13f2d5d7aa80fdbe56) by williamfzc).


## [v0.15.1](https://github.com/williamfzc/stagesepx/releases/tag/v0.15.1) - 2020-11-07

<small>[Compare with v0.15.0](https://github.com/williamfzc/stagesepx/compare/v0.15.0...v0.15.1)</small>

### Bug Fixes
- Change default values of keras train ([c44b6fd](https://github.com/williamfzc/stagesepx/commit/c44b6fdfd22b7b02775db9f1fc84b5ede45dfb68) by williamfzc).

### Features
- Verify dataset before train ([cb78e27](https://github.com/williamfzc/stagesepx/commit/cb78e27c835502b61b726ad143bbfeb32cfa4c5a) by williamfzc).


## [v0.15.0](https://github.com/williamfzc/stagesepx/releases/tag/v0.15.0) - 2020-09-07

<small>[Compare with v0.14.2](https://github.com/williamfzc/stagesepx/compare/v0.14.2...v0.15.0)</small>

### Bug Fixes
- Sync signatures ([63eac2e](https://github.com/williamfzc/stagesepx/commit/63eac2e9edbe8153ce2ddcb1189dca2135030e7b) by williamfzc).
- Remove unused command ([d21bfa6](https://github.com/williamfzc/stagesepx/commit/d21bfa6d6b1e5f4bbd79e801cffa9f400ff012de) by williamfzc).

### Code Refactoring
- Remove deprecated api ([967a08c](https://github.com/williamfzc/stagesepx/commit/967a08c2e907a8a8703269351bb1b877de59f7c3) by williamfzc).

### Features
- Ignore_error in calc ([6ed342b](https://github.com/williamfzc/stagesepx/commit/6ed342b6744514102348858f5de71500a9e2e822) by williamfzc).
- Path check first ([504667b](https://github.com/williamfzc/stagesepx/commit/504667b163a684e2854a3091ee3a981d5351cf0b) by williamfzc).
- Calcconfig ([8043f57](https://github.com/williamfzc/stagesepx/commit/8043f575880d5883521d9977fbaa09da59c8b201) by williamfzc).
- Api `contain` ([b6e5d05](https://github.com/williamfzc/stagesepx/commit/b6e5d0533d731f1ab040b90f2b7c2d76215c6161) by williamfzc).
- Remove `pre_load` and use `load_frames` instead ([3e1f673](https://github.com/williamfzc/stagesepx/commit/3e1f673d04f24536f19af24b1e20640a62ee9575) by williamfzc).
- Enable video preload by default ([dd2adec](https://github.com/williamfzc/stagesepx/commit/dd2adec7a0d9a8eb27db1b7974ac5394941afc42) by williamfzc).
- Extraconfig ([7f2517c](https://github.com/williamfzc/stagesepx/commit/7f2517cfef32723856c35361c1918d9bf1ade68c) by williamfzc).
- Videoconfig ([98cb9e6](https://github.com/williamfzc/stagesepx/commit/98cb9e68d291538fe32aab8aed46a224d895d41e) by williamfzc).
- Custom `compare_frame_list` method ([d215134](https://github.com/williamfzc/stagesepx/commit/d21513495980f82af6e0b47aaf487d352562d5b7) by williamfzc).
- `run` method accepts a path or a preload dict ([e64b983](https://github.com/williamfzc/stagesepx/commit/e64b98395386cafff4d5c8df7a31a78c87d045e7) by williamfzc).
- Run with config file ([829659b](https://github.com/williamfzc/stagesepx/commit/829659bca957155ebcd5ca9befd536615c227db8) by williamfzc).


## [v0.14.2](https://github.com/williamfzc/stagesepx/releases/tag/v0.14.2) - 2020-08-06

<small>[Compare with v0.14.1](https://github.com/williamfzc/stagesepx/compare/v0.14.1...v0.14.2)</small>

### Bug Fixes
- Support target_size in `draw` ([28cd4dc](https://github.com/williamfzc/stagesepx/commit/28cd4dc6ed2dd81fe94c91ce9fa2c5fcbdcb185f) by williamfzc).
- Reversed size ([802bd98](https://github.com/williamfzc/stagesepx/commit/802bd9870814ce81e480f6df0c83004ce35b767f) by williamfzc).
- Hook should always be applied in all the frames ([3184a0e](https://github.com/williamfzc/stagesepx/commit/3184a0e948cbc019be7312c54522849ad72d8ed9) by williamfzc).
- Size and count should be updated after hook ([2d28a63](https://github.com/williamfzc/stagesepx/commit/2d28a63f0545ee222a54ea1a98609ac62e05b3df) by williamfzc).


## [v0.14.1](https://github.com/williamfzc/stagesepx/releases/tag/v0.14.1) - 2020-07-18

<small>[Compare with v0.14.0](https://github.com/williamfzc/stagesepx/compare/v0.14.0...v0.14.1)</small>

### Features
- Support preload hook for video object ([c7af279](https://github.com/williamfzc/stagesepx/commit/c7af2797b8c68aa384bd0b756dd1bab94b57c011) by williamfzc).


## [v0.14.0](https://github.com/williamfzc/stagesepx/releases/tag/v0.14.0) - 2020-06-12

<small>[Compare with v0.13.1](https://github.com/williamfzc/stagesepx/compare/v0.13.1...v0.14.0)</small>

### Bug Fixes
- Do not wrap too much ([875ae42](https://github.com/williamfzc/stagesepx/commit/875ae42bd9a5a5058fa360d386e5351fe645c6ab) by williamfzc).
- Report path ends with .html ([e5875a9](https://github.com/williamfzc/stagesepx/commit/e5875a984cada35eaea99514ff9290add3e2d855) by williamfzc).
- Report path can be a directory ([ae93a2b](https://github.com/williamfzc/stagesepx/commit/ae93a2b7b0dc48b4c7db2b8a6cdd04c9692d8795) by williamfzc).
- Set parallel to 3 ([d035fda](https://github.com/williamfzc/stagesepx/commit/d035fda0273ca1f758ad5af5a4d8a98a6e89e1ea) by williamfzc).
- Stable api ([51b239a](https://github.com/williamfzc/stagesepx/commit/51b239aeaeb2cfbbb87b1617112f45f0a31ea8e0) by williamfzc).

### Features
- Cmd shortcut ([920a1c2](https://github.com/williamfzc/stagesepx/commit/920a1c2cacbe6eda5a5936be342926c21d738e6e) by williamfzc).
- Add py38 ([36b076a](https://github.com/williamfzc/stagesepx/commit/36b076adca62d506bee66c32e1c919217f52e98e) by williamfzc).


## [v0.13.1](https://github.com/williamfzc/stagesepx/releases/tag/v0.13.1) - 2020-05-25

<small>[Compare with v0.12.1](https://github.com/williamfzc/stagesepx/compare/v0.12.1...v0.13.1)</small>

### Features
- Very effective boost mode for all classifiers ([2d1cf1c](https://github.com/williamfzc/stagesepx/commit/2d1cf1c822be2cade101d8f58764a51f649773d4) by williamfzc).


## [v0.12.1](https://github.com/williamfzc/stagesepx/releases/tag/v0.12.1) - 2020-04-27

<small>[Compare with v0.12.0](https://github.com/williamfzc/stagesepx/compare/v0.12.0...v0.12.1)</small>

### Bug Fixes
- Add warning in report ([ad66a90](https://github.com/williamfzc/stagesepx/commit/ad66a904b64f8ae7dbbcf2b87d5fae2921e5d145) by williamfzc).

### Features
- Save trained model to random path if existed ([1e09e6d](https://github.com/williamfzc/stagesepx/commit/1e09e6d359653eb40bf9782b0a2d96ca7a4accae) by williamfzc).


## [v0.12.0](https://github.com/williamfzc/stagesepx/releases/tag/v0.12.0) - 2020-04-02

<small>[Compare with v0.11.2](https://github.com/williamfzc/stagesepx/compare/v0.11.2...v0.12.0)</small>

### Bug Fixes
- Error when step != 1 ([4de619a](https://github.com/williamfzc/stagesepx/commit/4de619a53d8ae5f0814fa866595e38823405c61e) by williamfzc).

### Features
- Sliding window ([e5845d2](https://github.com/williamfzc/stagesepx/commit/e5845d2211d2c60ecbb2a146cca625b114e343d8) by williamfzc).
- Dynamic range ([721cc69](https://github.com/williamfzc/stagesepx/commit/721cc69d2178d877a643983a2f1198999b664948) by williamfzc).


## [v0.11.2](https://github.com/williamfzc/stagesepx/releases/tag/v0.11.2) - 2020-03-22

<small>[Compare with v0.11.1](https://github.com/williamfzc/stagesepx/compare/v0.11.1...v0.11.2)</small>

### Bug Fixes
- Unstable and unspecific ([b3eea51](https://github.com/williamfzc/stagesepx/commit/b3eea5187204abbe7fdb4f1383aad5bf92e051d1) by williamfzc).
- Type error ([6fc668c](https://github.com/williamfzc/stagesepx/commit/6fc668c590f413610f029bc82afc3c90e312fb16) by williamfzc).
- Pathlib issue in videoobject ([b11041d](https://github.com/williamfzc/stagesepx/commit/b11041dbbb24c07b71eed88316406977a925248e) by williamfzc).

### Features
- New `helper` tab for report.html ([1406f68](https://github.com/williamfzc/stagesepx/commit/1406f682d93ad4b47be0041f50f8a67977e37687) by williamfzc).
- Add dump() for classifierresult ([212bb91](https://github.com/williamfzc/stagesepx/commit/212bb91c11c17054a358365d7d9c6db0073e86d1) by iceyhuang).


## [v0.11.1](https://github.com/williamfzc/stagesepx/releases/tag/v0.11.1) - 2020-03-10

<small>[Compare with v0.11.0](https://github.com/williamfzc/stagesepx/compare/v0.11.0...v0.11.1)</small>

### Bug Fixes
- Numpy version ([37b2765](https://github.com/williamfzc/stagesepx/commit/37b276594d6692b6f15ec931674bbc4d2e6beded) by williamfzc).
- Typing error ([3396d40](https://github.com/williamfzc/stagesepx/commit/3396d40321af9dcfc6189348248917f8f20cf3b4) by williamfzc).

### Features
- Time_cost_between() for quick calc ([6fd7460](https://github.com/williamfzc/stagesepx/commit/6fd74602e3675d4a632fe2dbe78d241f7f7f8c89) by williamfzc).


## [v0.11.0](https://github.com/williamfzc/stagesepx/releases/tag/v0.11.0) - 2020-03-02

<small>[Compare with v0.10.4](https://github.com/williamfzc/stagesepx/compare/v0.10.4...v0.11.0)</small>

### Bug Fixes
- Error if video has an unstable end ([b1e222d](https://github.com/williamfzc/stagesepx/commit/b1e222dac468d0fe400d9a0914307b98a566fe54) by williamfzc).
- Final stage ([1e6adc1](https://github.com/williamfzc/stagesepx/commit/1e6adc1f04c857fe35c450f195fee22118fb276a) by williamfzc).
- Get_stage_range ([46d2e46](https://github.com/williamfzc/stagesepx/commit/46d2e4694d073d86c960286cca27a27d209db482) by williamfzc).
- Timestamp ([c6dc3ad](https://github.com/williamfzc/stagesepx/commit/c6dc3ad51c27c1d555e66feab790d923866b140d) by williamfzc).
- About how pointer moving between frames ([3329eb9](https://github.com/williamfzc/stagesepx/commit/3329eb909f3e94fd530f622f0e11d204e2cda483) by williamfzc).
- Pointer offset ([b2be6f2](https://github.com/williamfzc/stagesepx/commit/b2be6f2d560c9226dbdd2bc8cbfd9d4c6d71666c) by williamfzc).
- Stage range error ([4511213](https://github.com/williamfzc/stagesepx/commit/4511213f73f5e8abb337c8895cab6405cc3310d7) by williamfzc).
- Meaning of timestamp ([22aef44](https://github.com/williamfzc/stagesepx/commit/22aef441bc7fe8c284544a5bbf3d33ffba18e58f) by williamfzc).

### Features
- Add extra frame in unstable range ([59c0815](https://github.com/williamfzc/stagesepx/commit/59c08158d4ed645996455fa655acff57236ab9f5) by williamfzc).
- Default threshold 0.95 -> 0.98 ([2259727](https://github.com/williamfzc/stagesepx/commit/22597276b230a1404d9bb0b9eba04a3732fb0ce8) by williamfzc).


## [v0.10.4](https://github.com/williamfzc/stagesepx/releases/tag/v0.10.4) - 2020-02-26

<small>[Compare with v0.10.3](https://github.com/williamfzc/stagesepx/compare/v0.10.3...v0.10.4)</small>

### Bug Fixes
- Wrong attr name ([078d12b](https://github.com/williamfzc/stagesepx/commit/078d12b10be7016f71590c15b526976fbd2f777f) by williamfzc).

### Code Refactoring
- Api for unstable range ([38ef721](https://github.com/williamfzc/stagesepx/commit/38ef721a2188c1597075f4be80d6e23a5dbc9725) by williamfzc).

### Features
- More api ([4fdda5c](https://github.com/williamfzc/stagesepx/commit/4fdda5c039e22f9b18cbf75ac08d3264c715b683) by williamfzc).


## [v0.10.3](https://github.com/williamfzc/stagesepx/releases/tag/v0.10.3) - 2020-02-19

<small>[Compare with v0.10.2](https://github.com/williamfzc/stagesepx/compare/v0.10.2...v0.10.3)</small>

### Bug Fixes
- Add tensorflow ([8c0bc44](https://github.com/williamfzc/stagesepx/commit/8c0bc44a11d27076ff8501882532235b2c69f52a) by williamfzc).
- Avoid conflict ([178c677](https://github.com/williamfzc/stagesepx/commit/178c6774acda43874051dc43a8723343a91972e5) by williamfzc).
- Lock opencv-contrib-python version ([7bfc2be](https://github.com/williamfzc/stagesepx/commit/7bfc2be64c449393f4b175fa162746680d623b7d) by williamfzc).
- Remove surf ([9f60be9](https://github.com/williamfzc/stagesepx/commit/9f60be97e953ba48cae930a4aa80c70b0ba7a75a) by williamfzc).

### Features
- Keras train function in command cli ([022eaa4](https://github.com/williamfzc/stagesepx/commit/022eaa4f155b9285690aca8d8251af9ec7ba1c37) by williamfzc).
- Add some warning msg when saving frames to a existed dir ([d678d7b](https://github.com/williamfzc/stagesepx/commit/d678d7b51d838e6825f6d6645825de9987b3c1e8) by williamfzc).
- Bump findit's version to 5.8 ([29d068e](https://github.com/williamfzc/stagesepx/commit/29d068e5587dc73e229303c1edc588e18daf63bb) by williamfzc).


## [v0.10.2](https://github.com/williamfzc/stagesepx/releases/tag/v0.10.2) - 2020-01-31

<small>[Compare with v0.10.1](https://github.com/williamfzc/stagesepx/compare/v0.10.1...v0.10.2)</small>

### Bug Fixes
- Raise exception when dir existed ([6408e26](https://github.com/williamfzc/stagesepx/commit/6408e267f3515926da1076f053fa6f390c0e2992) by williamfzc).


## [v0.10.1](https://github.com/williamfzc/stagesepx/releases/tag/v0.10.1) - 2020-01-19

<small>[Compare with v0.10.0](https://github.com/williamfzc/stagesepx/compare/v0.10.0...v0.10.1)</small>

### Bug Fixes
- Use notimplementederror in abstract methods ([39e0455](https://github.com/williamfzc/stagesepx/commit/39e045543258b2c29deab8e2b69197d8b7b9d51a) by williamfzc).
- Length check ([038a829](https://github.com/williamfzc/stagesepx/commit/038a82970812e541cd901442ba376c9046ebbd2c) by williamfzc).

### Features
- Meaningful image names ([d70ac78](https://github.com/williamfzc/stagesepx/commit/d70ac785ddfbf006bbf6de21f6d685faa126186a) by williamfzc).


## [v0.10.0](https://github.com/williamfzc/stagesepx/releases/tag/v0.10.0) - 2020-01-12

<small>[Compare with v0.9.4](https://github.com/williamfzc/stagesepx/compare/v0.9.4...v0.10.0)</small>

### Bug Fixes
- Wrong way to use model ([1e63c49](https://github.com/williamfzc/stagesepx/commit/1e63c49f69f8a354f84d98f5449b4030fb17751e) by williamfzc).
- Use sparse_categorical_crossentropy ([cc4f737](https://github.com/williamfzc/stagesepx/commit/cc4f73795f16e4c7b733f5411935de8ebffb0360) by williamfzc).
- Turn_binary ([bcd585c](https://github.com/williamfzc/stagesepx/commit/bcd585cd701957f8b76f260d054af93482d482a1) by williamfzc).
- Keras setup ([f02286d](https://github.com/williamfzc/stagesepx/commit/f02286dd318839a821c01299f70aedcd4e5d8ec2) by williamfzc).
- Model design ([498e949](https://github.com/williamfzc/stagesepx/commit/498e94956122d8930351d48e9ddb10e6a42ae88b) by williamfzc).

### Code Refactoring
- Add basemodelclassifier for extending ([1f996fd](https://github.com/williamfzc/stagesepx/commit/1f996fde191ddf266375adbcef555cf4258f3b7c) by williamfzc).

### Features
- Basic keras classifier ([e9059cf](https://github.com/williamfzc/stagesepx/commit/e9059cfe17b6e1fbd05e8c029eca9b71500737d1) by williamfzc).


## [v0.9.4](https://github.com/williamfzc/stagesepx/releases/tag/v0.9.4) - 2020-01-02

<small>[Compare with v0.9.3](https://github.com/williamfzc/stagesepx/compare/v0.9.3...v0.9.4)</small>

### Bug Fixes
- Handle hooks at the beginning ([6c4c612](https://github.com/williamfzc/stagesepx/commit/6c4c612f19e327ed247cc11f2d540f4e3372bd81) by williamfzc).

### Features
- New api for important frames ([72b2d03](https://github.com/williamfzc/stagesepx/commit/72b2d03f859df34103dc5c101b8093342438bdde) by williamfzc).


## [v0.9.3](https://github.com/williamfzc/stagesepx/releases/tag/v0.9.3) - 2019-12-26

<small>[Compare with v0.9.2](https://github.com/williamfzc/stagesepx/compare/v0.9.2...v0.9.3)</small>

### Bug Fixes
- Remove `overwrite` ([f9abb41](https://github.com/williamfzc/stagesepx/commit/f9abb414218ff31647f0cea040420a3aaf7bb4e6) by williamfzc).

### Features
- Better file name for framesavehook ([4740bbf](https://github.com/williamfzc/stagesepx/commit/4740bbf4c6649a8b63b8d8f4765460cedf4b24bc) by williamfzc).
- Better hook design ([00193dc](https://github.com/williamfzc/stagesepx/commit/00193dcb2edbc9b3c17bb685b063c0275e7db6a3) by williamfzc).


## [v0.9.2](https://github.com/williamfzc/stagesepx/releases/tag/v0.9.2) - 2019-12-17

<small>[Compare with v0.9.1](https://github.com/williamfzc/stagesepx/compare/v0.9.1...v0.9.2)</small>

### Bug Fixes
- Resize the video length after load_frames ([1817cb7](https://github.com/williamfzc/stagesepx/commit/1817cb7a917ee5e4dfbf4ddfc6cfbf1f62e5cffa) by williamfzc).
- For actions/virtual-environments ([9ef6a3d](https://github.com/williamfzc/stagesepx/commit/9ef6a3d938c16df77a85c706855a8714eb934ae2) by williamfzc).
- Better support for findit ([ac027b1](https://github.com/williamfzc/stagesepx/commit/ac027b1f9aec23bd3d99e7c48f1bc31dd504351a) by williamfzc).
- 3.7.5 > 3.7 in setup.py ([f75ae67](https://github.com/williamfzc/stagesepx/commit/f75ae67da730a5e11ed8508bac788b928adf7ed6) by williamfzc).

### Features
- To_dict return ordereddict ([e736642](https://github.com/williamfzc/stagesepx/commit/e73664226e3f3ad0e42ffd2d8c9372bc37d11286) by williamfzc).


## [v0.9.1](https://github.com/williamfzc/stagesepx/releases/tag/v0.9.1) - 2019-12-05

<small>[Compare with v0.9.0](https://github.com/williamfzc/stagesepx/compare/v0.9.0...v0.9.1)</small>

### Bug Fixes
- Error case ([b3f2541](https://github.com/williamfzc/stagesepx/commit/b3f2541daff649164370ed2401ccbf72b8415c5f) by williamfzc).
- Contain_image allow kwargs only (for extra args in findit) ([1c9f989](https://github.com/williamfzc/stagesepx/commit/1c9f9898aec796b368756b419e21180acc409973) by williamfzc).

### Code Refactoring
- Move match_template to toolbox.py ([bb06077](https://github.com/williamfzc/stagesepx/commit/bb060777df3435f25271c04b67544caa6ca8021f) by williamfzc).

### Features
- Support contain_image in singleclassifierresult ([d9aee84](https://github.com/williamfzc/stagesepx/commit/d9aee841f0460343b28d7e2017618d4b636ba27a) by williamfzc).
- Extra args (optional) for contain_image ([ae04813](https://github.com/williamfzc/stagesepx/commit/ae048131711da08e617f136da48a06c394dd0460) by williamfzc).
- Support contain_image in videoframe ([16b70eb](https://github.com/williamfzc/stagesepx/commit/16b70eb1d69d407ee695735c56f438e9c13964f7) by williamfzc).


## [v0.9.0](https://github.com/williamfzc/stagesepx/releases/tag/v0.9.0) - 2019-11-22

<small>[Compare with v0.8.4](https://github.com/williamfzc/stagesepx/compare/v0.8.4...v0.9.0)</small>

### Bug Fixes
- Error assertion ([7d2b1b9](https://github.com/williamfzc/stagesepx/commit/7d2b1b9de0dbbee55d72021d37674d3fd6fbaac1) by williamfzc).
- Remove unused cases ([a0373f9](https://github.com/williamfzc/stagesepx/commit/a0373f9d7181d6968d9d7aa04cdbfa8272c844ae) by williamfzc).
- Duration is hard to understand ([6a29656](https://github.com/williamfzc/stagesepx/commit/6a29656b54d249409fce62e3d7c6b3110802d341) by williamfzc).
- Ffmpeg need `sudo` ([a80ef82](https://github.com/williamfzc/stagesepx/commit/a80ef82cc02530d988340f779e9f6a49b31fc719) by williamfzc).
- Install ffmpeg firstly ([2cae8c4](https://github.com/williamfzc/stagesepx/commit/2cae8c40dbc1061445135e767145ff49f143792f) by williamfzc).

### Code Refactoring
- Put all the flags to constants.py ([6dcac6a](https://github.com/williamfzc/stagesepx/commit/6dcac6a86c4f42ba0eb952883c8e0191da276461) by williamfzc).
- New `draw` function ([c6fcf32](https://github.com/williamfzc/stagesepx/commit/c6fcf327ed79220b59138af53abe4b0f94c867df) by williamfzc).
- Render with classifier result only ([864c178](https://github.com/williamfzc/stagesepx/commit/864c178d8e27b6e45217cc0ca30e778081ca3d43) by williamfzc).

### Features
- Video info in report ([5f37bb5](https://github.com/williamfzc/stagesepx/commit/5f37bb5dda37a224fdb54131ed1b9d5edf6a6a5e) by williamfzc).
- New design for easily review :) ([1dc857f](https://github.com/williamfzc/stagesepx/commit/1dc857f28a13ee8d96305a5700e08e303d5fe1a2) by williamfzc).
- Support portable ffmpeg ([2c0a5e7](https://github.com/williamfzc/stagesepx/commit/2c0a5e765736fa8ea7b9886bd148aa06e9a9a6cb) by williamfzc).
- Ffmpeg converter ([df13699](https://github.com/williamfzc/stagesepx/commit/df13699a183285785338af6a08dcb8d2fe177a59) by williamfzc).


## [v0.8.4](https://github.com/williamfzc/stagesepx/releases/tag/v0.8.4) - 2019-11-18

<small>[Compare with v0.8.3](https://github.com/williamfzc/stagesepx/compare/v0.8.3...v0.8.4)</small>

### Bug Fixes
- Remove python 3.8 ([707aad9](https://github.com/williamfzc/stagesepx/commit/707aad96c5456629ba829fa2a86b4489ac70f39d) by williamfzc).
- Error in cases ([69e1c39](https://github.com/williamfzc/stagesepx/commit/69e1c39f0b8f2c7578ebe7674c8873af15cf3430) by williamfzc).

### Features
- Flexible blocks ([fbd0ab9](https://github.com/williamfzc/stagesepx/commit/fbd0ab9653fbbe365aa5553b21e6230cabd6c686) by williamfzc).


## [v0.8.3](https://github.com/williamfzc/stagesepx/releases/tag/v0.8.3) - 2019-11-05

<small>[Compare with v0.8.2](https://github.com/williamfzc/stagesepx/compare/v0.8.2...v0.8.3)</small>

### Bug Fixes
- Pyecharts can not handle float list directly ([29f3d32](https://github.com/williamfzc/stagesepx/commit/29f3d32d8b3b594181a1c78a70652057598fe165) by williamfzc).
- Miss thumbnail in mini.py ([bf250ac](https://github.com/williamfzc/stagesepx/commit/bf250ac3edfa98dad499d70dc42eb397c0ce01a7) by williamfzc).
- Video_jump does not lead to correct point ([e6e78a4](https://github.com/williamfzc/stagesepx/commit/e6e78a4a714c44d8124f997e5d2be1a999810d50) by williamfzc).


## [v0.8.2](https://github.com/williamfzc/stagesepx/releases/tag/v0.8.2) - 2019-10-26

<small>[Compare with v0.8.1](https://github.com/williamfzc/stagesepx/compare/v0.8.1...v0.8.2)</small>

### Bug Fixes
- Sync example ([5cff6ba](https://github.com/williamfzc/stagesepx/commit/5cff6bad427459ee70e35d98fe49206362df5254) by williamfzc).
- Sync test cases ([dce9edf](https://github.com/williamfzc/stagesepx/commit/dce9edfd8b5518e9839d6638f58457c36c3dd58e) by williamfzc).
- Lock python image version to 3.7 ([d54d509](https://github.com/williamfzc/stagesepx/commit/d54d5092c1580958b845c3685ef0da34a221021d) by williamfzc).
- Opencv-python version ([43a14a1](https://github.com/williamfzc/stagesepx/commit/43a14a1b6c81be0f41e5f53c655e61b95e5f19fa) by williamfzc).
- Lock opencv-python version to 4.1.0.25 ([0a8e8e1](https://github.com/williamfzc/stagesepx/commit/0a8e8e1fdd8c18e63134edddad69e7e039d94cf5) by williamfzc).

### Code Refactoring
- Output of classifier has became an classifierresult object, not a list ([6cec3e8](https://github.com/williamfzc/stagesepx/commit/6cec3e8a620ed105a2fe232855848265018cc5a4) by williamfzc).


## [v0.8.1](https://github.com/williamfzc/stagesepx/releases/tag/v0.8.1) - 2019-10-14

<small>[Compare with v0.8.0](https://github.com/williamfzc/stagesepx/compare/v0.8.0...v0.8.1)</small>

### Bug Fixes
- Skimage version 0.14.2 to 0.16.0 ([c85d62d](https://github.com/williamfzc/stagesepx/commit/c85d62d58cd2559d77e965efc928f57803eb5c70) by williamfzc).
- Dead loop occasionally ([d57a29c](https://github.com/williamfzc/stagesepx/commit/d57a29c6ac60d77b7ad9d849fd15767b0d91d938) by williamfzc).
- Rename emptyframedetecthook to interestpointhook ([be24630](https://github.com/williamfzc/stagesepx/commit/be24630b2b03a42db2f54a1d6001c2b19c6bdc9f) by williamfzc).
- Type warning from `pyright` ([aeb81a5](https://github.com/williamfzc/stagesepx/commit/aeb81a5e96fe90da9a7c7e04a28e9a005ad252be) by williamfzc).

### Features
- Add pre_load option in __init__ ([9f34692](https://github.com/williamfzc/stagesepx/commit/9f3469295fe7fa6d69553301e578f7fd97123fcb) by williamfzc).
- Support emptyframedetecthook ([ba8ef2a](https://github.com/williamfzc/stagesepx/commit/ba8ef2aa704f89f060c3ac60cdcb8df38266fb6c) by williamfzc).
- Add version code at the footer of report ([175d855](https://github.com/williamfzc/stagesepx/commit/175d855aa7839b0386e8dea5269b56b3a79d0e7d) by williamfzc).


## [v0.8.0](https://github.com/williamfzc/stagesepx/releases/tag/v0.8.0) - 2019-09-26

<small>[Compare with v0.7.5](https://github.com/williamfzc/stagesepx/compare/v0.7.5...v0.8.0)</small>

### Bug Fixes
- Error import ([665f2ca](https://github.com/williamfzc/stagesepx/commit/665f2ca98f2bb10c107af638aa18ae62b34e0b1a) by williamfzc).
- Avoid import loop ([78dc9b3](https://github.com/williamfzc/stagesepx/commit/78dc9b3efd222c08893edc979e5f2901977cedc0) by williamfzc).
- Bug found by unittest ([43032f2](https://github.com/williamfzc/stagesepx/commit/43032f247850585d3426a0a184f049b8adfb982f) by williamfzc).
- Error because of numpy.ndarray -> json ([e9d4dc4](https://github.com/williamfzc/stagesepx/commit/e9d4dc4c366abc7c2aab61ea618661bffc5888d0) by williamfzc).

### Code Refactoring
- Cutter ([9fb3377](https://github.com/williamfzc/stagesepx/commit/9fb3377d66c579b90c5f0a6a7ff5f9e2b66a90de) by williamfzc).

### Features
- Support videoobject in api.py ([c4a0182](https://github.com/williamfzc/stagesepx/commit/c4a0182657f9aac90ceb87a98d47bd3e6033fb01) by williamfzc).
- Support videoobject in cut and classify ([25e26b4](https://github.com/williamfzc/stagesepx/commit/25e26b4264e8bf25140c06a5988eab6b80e9cfec) by williamfzc).
- Add videoframe / videooperator / videoobject ([41c9d68](https://github.com/williamfzc/stagesepx/commit/41c9d688197c0f50d0a11eb18bde6b22d2d5e101) by williamfzc).


## [v0.7.5](https://github.com/williamfzc/stagesepx/releases/tag/v0.7.5) - 2019-09-24

<small>[Compare with v0.7.4](https://github.com/williamfzc/stagesepx/compare/v0.7.4...v0.7.5)</small>

### Bug Fixes
- Always cut before classify ([3d83c5d](https://github.com/williamfzc/stagesepx/commit/3d83c5db1bd703acb4a33394c43b5dda7e92235d) by williamfzc).
- Classify with trained model failed ([8f7dc18](https://github.com/williamfzc/stagesepx/commit/8f7dc18dfe660d7c0254ebb75955381157205932) by williamfzc).
- Miss `train` in __all__ ([8c791ad](https://github.com/williamfzc/stagesepx/commit/8c791adb9ef7d88b2ca88e0bef15fc969c463746) by williamfzc).


## [v0.7.4](https://github.com/williamfzc/stagesepx/releases/tag/v0.7.4) - 2019-09-24

<small>[Compare with v0.7.3](https://github.com/williamfzc/stagesepx/compare/v0.7.3...v0.7.4)</small>

### Bug Fixes
- Model name conflict ([9d55e92](https://github.com/williamfzc/stagesepx/commit/9d55e928309cc9c2f4ffa290fc5b330aa864eb2e) by williamfzc).
- Add test cases for `train` in api ([c009dcc](https://github.com/williamfzc/stagesepx/commit/c009dcccf54d03aaec7c7ac19637ed5a45cfb457) by williamfzc).

### Code Refactoring
- Less code, better structure ([5605a1e](https://github.com/williamfzc/stagesepx/commit/5605a1e8e581f07c32e1af410e1e1a869f48aaf1) by williamfzc).
- Split cli.py into 2 files ([815f899](https://github.com/williamfzc/stagesepx/commit/815f899ba1352ab3caa45a0b747d0817065c5842) by williamfzc).
- Split cli.py into cli and api ([ded8a73](https://github.com/williamfzc/stagesepx/commit/ded8a73e21c8b208565c0e092250eac13e99d29b) by williamfzc).

### Features
- Support `train` ([af05c72](https://github.com/williamfzc/stagesepx/commit/af05c7217c9d6f7718c8da69c531a3480466c391) by williamfzc).
- Support classifying with a trained model ([98411ef](https://github.com/williamfzc/stagesepx/commit/98411efea580b445e41ce8af3d1884d0836f87fc) by williamfzc).

### Reverts
- No need ([495107e](https://github.com/williamfzc/stagesepx/commit/495107ea435e61bd67957c117eb1a594a0f34e79) by williamfzc).


## [v0.7.3](https://github.com/williamfzc/stagesepx/releases/tag/v0.7.3) - 2019-09-17

<small>[Compare with v0.7.2](https://github.com/williamfzc/stagesepx/compare/v0.7.2...v0.7.3)</small>

### Features
- Support chinese report ([7a9656f](https://github.com/williamfzc/stagesepx/commit/7a9656fcbd1191f9b843031f7d2880d953712873) by williamfzc).
- Support `save` and `load` in reporter ([b19ff7d](https://github.com/williamfzc/stagesepx/commit/b19ff7d63c114730378a3b1212b99b33aeaeee51) by williamfzc).


## [v0.7.2](https://github.com/williamfzc/stagesepx/releases/tag/v0.7.2) - 2019-09-10

<small>[Compare with v0.7.1](https://github.com/williamfzc/stagesepx/compare/v0.7.1...v0.7.2)</small>


## [v0.7.1](https://github.com/williamfzc/stagesepx/releases/tag/v0.7.1) - 2019-09-10

<small>[Compare with v0.7.0](https://github.com/williamfzc/stagesepx/compare/v0.7.0...v0.7.1)</small>

### Bug Fixes
- Replace `cv2.imread` with `toolbox.imread` ([f360212](https://github.com/williamfzc/stagesepx/commit/f360212fcc1657bea3f613b00739bd4eb38e17ca) by williamfzc).
- Do not run cli in shell ([697129a](https://github.com/williamfzc/stagesepx/commit/697129a17b48c83720929dc5bbf2535c7333bb2b) by williamfzc).
- (try to) using py.test with coverage doesn't include imports ([bc8ec3d](https://github.com/williamfzc/stagesepx/commit/bc8ec3dc001f91087c64c52085946b129f917022) by williamfzc).
- Video path ([e601912](https://github.com/williamfzc/stagesepx/commit/e6019128704abc03f0d4e36c3a14f8a505ffdbbd) by williamfzc).
- Github actions pipeline ([c6ae64a](https://github.com/williamfzc/stagesepx/commit/c6ae64a36ea906a5d2dd1ed52653985c414589ec) by williamfzc).

### Code Refactoring
- Case structure improvement ([2c51277](https://github.com/williamfzc/stagesepx/commit/2c51277f231bc9b5313b73823b671847a0b34ad5) by williamfzc).

### Features
- Support ignorehook! ([3f81c77](https://github.com/williamfzc/stagesepx/commit/3f81c77b1b4332f50052e3435609e5f4040f6253) by williamfzc).


## [v0.7.0](https://github.com/williamfzc/stagesepx/releases/tag/v0.7.0) - 2019-09-08

<small>[Compare with v0.6.2](https://github.com/williamfzc/stagesepx/compare/v0.6.2...v0.7.0)</small>

### Bug Fixes
- In the binary case, return type is different (wtf ...) ([a8de2bd](https://github.com/williamfzc/stagesepx/commit/a8de2bdf2ebe3d9b3c0c2597255aea19cc78df58) by williamfzc).
- Default thumbnail maybe different (no args and kwargs) ([127193d](https://github.com/williamfzc/stagesepx/commit/127193d525e4f6db67a3dc8e69aaacbb207d83a3) by williamfzc).

### Features
- Support crophook! ([68a4b2f](https://github.com/williamfzc/stagesepx/commit/68a4b2f322b60b5b89eb5ac61ba834bd76e86b58) by williamfzc).
- Add duration data in thumbnail ([8d70fa2](https://github.com/williamfzc/stagesepx/commit/8d70fa230483ccff8efbdb300a142556c5bc8121) by williamfzc).
- Support score_threshold ([b2d5ba7](https://github.com/williamfzc/stagesepx/commit/b2d5ba7e36e1919a8c4b5e5faccb3e9f63a1075a) by williamfzc).
- Add scores of each stages in log ([cc899a7](https://github.com/williamfzc/stagesepx/commit/cc899a727303d318c66873890b11fbd03a3240b0) by williamfzc).


## [v0.6.2](https://github.com/williamfzc/stagesepx/releases/tag/v0.6.2) - 2019-09-04

<small>[Compare with v0.6.1](https://github.com/williamfzc/stagesepx/compare/v0.6.1...v0.6.2)</small>

### Features
- Support offset ([c902361](https://github.com/williamfzc/stagesepx/commit/c9023616bcd67cdc06b719cf4fa0915aa6c8a274) by williamfzc).
- Official docker image ([0b03423](https://github.com/williamfzc/stagesepx/commit/0b03423a00efecf5e8e26d6f9396a2bc84c768f2) by williamfzc).


## [v0.6.1](https://github.com/williamfzc/stagesepx/releases/tag/v0.6.1) - 2019-09-01

<small>[Compare with v0.6.0](https://github.com/williamfzc/stagesepx/compare/v0.6.0...v0.6.1)</small>

### Bug Fixes
- Default compress rate ([feb4351](https://github.com/williamfzc/stagesepx/commit/feb4351dca0a5bc09ff4f0fb518b8529f1f68b64) by williamfzc).
- Default compress rate is none ([dc3c850](https://github.com/williamfzc/stagesepx/commit/dc3c850c871a7d45e71ac0a86d1dfec74d7431a0) by williamfzc).

### Code Refactoring
- Better tutorial ([8cd3e9d](https://github.com/williamfzc/stagesepx/commit/8cd3e9d85b4d9165f65fd659c7fac1161ad81579) by williamfzc).

### Features
- Threshold in kwargs ([b011073](https://github.com/williamfzc/stagesepx/commit/b011073e23810d3a14c725e93fc796470b02e288) by williamfzc).
- Test for cli ([2d87c2d](https://github.com/williamfzc/stagesepx/commit/2d87c2de59068713e07fbd250135288cf0a9ada7) by williamfzc).
- Support base classifier api ([0991505](https://github.com/williamfzc/stagesepx/commit/09915052b25e9c5bba26de3037e2e5d2058300c8) by williamfzc).
- Finish cut api ([9592475](https://github.com/williamfzc/stagesepx/commit/959247550058dbcd1c3376277c52e28dcd90187c) by williamfzc).
- Finish one-step api ([7bacd03](https://github.com/williamfzc/stagesepx/commit/7bacd03487c2cc51c7f86af7adff92325598f836) by williamfzc).
- Add cli test in workflow ([24745ed](https://github.com/williamfzc/stagesepx/commit/24745edb1ec8ca6fcdad1f2323b3efcb4a63707f) by williamfzc).
- Base cli for terminal! ([9d2bb54](https://github.com/williamfzc/stagesepx/commit/9d2bb54e1c9ae7ca0b5740d50edfdf1b548c6306) by williamfzc).
- Limit in stable ranges and unstable ranges ([fea1d85](https://github.com/williamfzc/stagesepx/commit/fea1d858e406c3e93fe5fb67dcce3780bafa8465) by williamfzc).


## [v0.6.0](https://github.com/williamfzc/stagesepx/releases/tag/v0.6.0) - 2019-08-30

<small>[Compare with v0.5.3](https://github.com/williamfzc/stagesepx/compare/v0.5.3...v0.6.0)</small>

### Bug Fixes
- Extra kwargs will not be used in diff ([689965d](https://github.com/williamfzc/stagesepx/commit/689965df3f21bbaf43dad417db1900a911a649e5) by williamfzc).
- When err == 0, psnr will be 'inf' ([d0e11f7](https://github.com/williamfzc/stagesepx/commit/d0e11f767c4ce9d63ed5c364f2438f7cf1d0a6cc) by williamfzc).

### Features
- Background color in report ([e1065d1](https://github.com/williamfzc/stagesepx/commit/e1065d1def6101406f9cdf64499cb6bbaf307f41) by williamfzc).
- Report improvement ([b6d8dec](https://github.com/williamfzc/stagesepx/commit/b6d8dece29334c7f6066c4d706b096089f6262b2) by williamfzc).
- Disable is_step ([0ccb3c5](https://github.com/williamfzc/stagesepx/commit/0ccb3c52b0532d2b543d7abdf074683388257390) by williamfzc).
- Time cost of stage changing ([fa47ba0](https://github.com/williamfzc/stagesepx/commit/fa47ba0f98745c56fdf2136df0b56ebcd4fb87a4) by williamfzc).
- Add split line in thumbnail ([7218dfd](https://github.com/williamfzc/stagesepx/commit/7218dfd309786553830e87fe8eaa249c3fd2bff5) by williamfzc).
- More info in return of diff ([3eed5bd](https://github.com/williamfzc/stagesepx/commit/3eed5bd6a040dafdaffa9514fafb3f9b1e169e5f) by williamfzc).
- Built-in thumbnail ([d3aaeeb](https://github.com/williamfzc/stagesepx/commit/d3aaeeb120d708a6c48c31be741a7724a8e1516e) by williamfzc).


## [v0.5.3](https://github.com/williamfzc/stagesepx/releases/tag/v0.5.3) - 2019-08-25

<small>[Compare with v0.5.2](https://github.com/williamfzc/stagesepx/compare/v0.5.2...v0.5.3)</small>

### Bug Fixes
- Github actions badge ([d96dbf2](https://github.com/williamfzc/stagesepx/commit/d96dbf2f61944a8b06a1b6a53e51b8521754a04b) by williamfzc).

### Features
- Set ssim + psnr as default ([b51dc00](https://github.com/williamfzc/stagesepx/commit/b51dc0056d6a596380878f9261acac9805474541) by williamfzc).
- Add psnr ([42309c2](https://github.com/williamfzc/stagesepx/commit/42309c2beb76a362e76c3141bc4aa541ff4bff4a) by williamfzc).
- Add sim chart ([78e8ec6](https://github.com/williamfzc/stagesepx/commit/78e8ec62dd92a7c13469d42bf2cf2d5c8e22a07f) by williamfzc).
- Add mse ([bd8286e](https://github.com/williamfzc/stagesepx/commit/bd8286ed4ece7605c2f1d1b00a855960c9b38e3f) by williamfzc).


## [v0.5.2](https://github.com/williamfzc/stagesepx/releases/tag/v0.5.2) - 2019-08-22

<small>[Compare with v0.5.1](https://github.com/williamfzc/stagesepx/compare/v0.5.1...v0.5.2)</small>

### Features
- Better sampling algorithm ([b512fa8](https://github.com/williamfzc/stagesepx/commit/b512fa82997eea98d38ba57fda330a407beb0d52) by williamfzc).


## [v0.5.1](https://github.com/williamfzc/stagesepx/releases/tag/v0.5.1) - 2019-08-18

<small>[Compare with v0.5.0](https://github.com/williamfzc/stagesepx/compare/v0.5.0...v0.5.1)</small>

### Code Refactoring
- Move all the frame-level operations to hook ([4fda59a](https://github.com/williamfzc/stagesepx/commit/4fda59ac5070ad4b77ac8e0ee81fc9ef2ca08789) by williamfzc).

### Features
- Support label 'overwrite' in hook ([694319a](https://github.com/williamfzc/stagesepx/commit/694319a622bbde57ad8984c7e2d357bcf1cdbda5) by williamfzc).


## [v0.5.0](https://github.com/williamfzc/stagesepx/releases/tag/v0.5.0) - 2019-08-16

<small>[Compare with v0.4.3](https://github.com/williamfzc/stagesepx/compare/v0.4.3...v0.5.0)</small>

### Bug Fixes
- Miss last stage ([75a7ab1](https://github.com/williamfzc/stagesepx/commit/75a7ab13dbce7492c34f77a83511d1ce0add38c4) by williamfzc).
- Timestamp error ([f08a467](https://github.com/williamfzc/stagesepx/commit/f08a46799ed22032a6714bd7203f153d733e55d4) by williamfzc).
- Remove data assertion before classify ([e7a4497](https://github.com/williamfzc/stagesepx/commit/e7a44975b433d027705f0a82d131112fd536b83c) by williamfzc).

### Features
- Support pruning redundant stages ([24cddc9](https://github.com/williamfzc/stagesepx/commit/24cddc956155e1f8157b20f0041d4497f2e50aae) by williamfzc).
- Support findit hook ([d1d8340](https://github.com/williamfzc/stagesepx/commit/d1d8340827a86eb867b84b7d233935045a4e8073) by williamfzc).
- Add option 'auto_merge' in diff function ([af7123d](https://github.com/williamfzc/stagesepx/commit/af7123d5be789f1dc5483f21d264b658f65ce895) by williamfzc).


## [v0.4.3](https://github.com/williamfzc/stagesepx/releases/tag/v0.4.3) - 2019-08-14

<small>[Compare with v0.4.2](https://github.com/williamfzc/stagesepx/compare/v0.4.2...v0.4.3)</small>

### Features
- Support diff in videocutresult ([8a014ae](https://github.com/williamfzc/stagesepx/commit/8a014aeb6b62fd18248b4a88aa34b4484781600e) by williamfzc).
- Support videoframe ([050efd1](https://github.com/williamfzc/stagesepx/commit/050efd1ec0bfe0555689d739426ece8f5d766c81) by williamfzc).
- Support load and dump ([913d78f](https://github.com/williamfzc/stagesepx/commit/913d78f95b3d3140b9352fd555c32eba6f2ac9e6) by williamfzc).


## [v0.4.2](https://github.com/williamfzc/stagesepx/releases/tag/v0.4.2) - 2019-08-11

<small>[Compare with v0.4.1](https://github.com/williamfzc/stagesepx/compare/v0.4.1...v0.4.2)</small>

### Bug Fixes
- Error when len(unstable_list) == 0 ([185abfc](https://github.com/williamfzc/stagesepx/commit/185abfcaf00337ebf8a4b2d3ffd87845df1a58b4) by williamfzc). Related issues/PRs: [#25](https://github.com/williamfzc/stagesepx/issues/25)

### Features
- Support invalid frame detect hook ([3fa8026](https://github.com/williamfzc/stagesepx/commit/3fa8026db5e679059c8ef72a31ccd67417219efc) by williamfzc).
- Support framesavehook ([0253304](https://github.com/williamfzc/stagesepx/commit/0253304ba9c9386f74dabc52f03a1033979b558b) by williamfzc).
- Support hook ([c3521a2](https://github.com/williamfzc/stagesepx/commit/c3521a27b0bf4fdc1a5a5bea237a03bf10d4fb92) by williamfzc).


## [v0.4.1](https://github.com/williamfzc/stagesepx/releases/tag/v0.4.1) - 2019-08-09

<small>[Compare with v0.4.0](https://github.com/williamfzc/stagesepx/compare/v0.4.0...v0.4.1)</small>

### Bug Fixes
- Frame id out of range ([98e64c4](https://github.com/williamfzc/stagesepx/commit/98e64c48aee24c6aec6dd0eb30185eb76d397a3a) by williamfzc).
- Wrong video name ([1110200](https://github.com/williamfzc/stagesepx/commit/11102009db0ceb5e12bcf0f40fe5305363389121) by williamfzc).

### Code Refactoring
- Use videoobject, not video path ([721503f](https://github.com/williamfzc/stagesepx/commit/721503fe4e62deb58f826bb4e81634a2b66e1c2f) by williamfzc).


## [v0.4.0](https://github.com/williamfzc/stagesepx/releases/tag/v0.4.0) - 2019-08-06

<small>[Compare with v0.3.3](https://github.com/williamfzc/stagesepx/compare/v0.3.3...v0.4.0)</small>

### Bug Fixes
- Error when unstable range count equal or less than 1 ([bb002bf](https://github.com/williamfzc/stagesepx/commit/bb002bfde30a2ca7cc397e99cf138ba6d908362e) by williamfzc).
- Index out of range ([635aa18](https://github.com/williamfzc/stagesepx/commit/635aa18f4e4b872e9d2f1a313ca85982bfc19607) by williamfzc).
- Range_threshold should be optional ([b2c6796](https://github.com/williamfzc/stagesepx/commit/b2c67966d58b09f226aba5a840a828e2ef826e85) by williamfzc).
- Error when video starts (ends) with changing ([dc1b208](https://github.com/williamfzc/stagesepx/commit/dc1b2085a54fc6e9f34a0995e49a823661b6131c) by williamfzc).
- Error when using compression ([dc3926a](https://github.com/williamfzc/stagesepx/commit/dc3926aac413450a338361134d5fe50bae1c9066) by williamfzc).

### Code Refactoring
- Too much code in cutter.py ([cd44b09](https://github.com/williamfzc/stagesepx/commit/cd44b0940bcd298258575e4d51104d60e7e31630) by williamfzc).

### Features
- Block cutter ([3ecb828](https://github.com/williamfzc/stagesepx/commit/3ecb828a02cdb3d71ea7aa50ff12a086c97a2ba8) by williamfzc).
- More precise comparison in cutter ([8b71435](https://github.com/williamfzc/stagesepx/commit/8b71435319e3ff738feaad3265c9ab8d79932df8) by williamfzc).
- Support comparison between different results of cutter ([87a378b](https://github.com/williamfzc/stagesepx/commit/87a378b310061e81d1f00c924617dd87c3d30406) by williamfzc).
- Support offset ([0a693bc](https://github.com/williamfzc/stagesepx/commit/0a693bc6fa120506718cbb2d1d4fbe2767fcb5ae) by williamfzc).
- Support range_threshold ([8275535](https://github.com/williamfzc/stagesepx/commit/8275535818ba287ad3fe00c73a0317d9332aa588) by williamfzc).
- Change self.ssim to a list of ssim value ([271a451](https://github.com/williamfzc/stagesepx/commit/271a451b65ca0f1efbe88ea2d39e5e9d15887eeb) by williamfzc).
- Need not get timestamp from video again ([1452525](https://github.com/williamfzc/stagesepx/commit/1452525a89b675faf86700fb5e81f25f3c66ae7a) by williamfzc).
- Timestamp in videocutrange ([feeaa67](https://github.com/williamfzc/stagesepx/commit/feeaa672ce702c3d8bf05609a086136ac005a941) by williamfzc).


## [v0.3.3](https://github.com/williamfzc/stagesepx/releases/tag/v0.3.3) - 2019-08-01

<small>[Compare with v0.3.2](https://github.com/williamfzc/stagesepx/compare/v0.3.2...v0.3.3)</small>

### Features
- Support specific size in compression ([f95a4df](https://github.com/williamfzc/stagesepx/commit/f95a4df96cc74e0288fbcf60ddcb6bef0929cee5) by williamfzc).


## [v0.3.2](https://github.com/williamfzc/stagesepx/releases/tag/v0.3.2) - 2019-07-28

<small>[Compare with v0.3.1](https://github.com/williamfzc/stagesepx/compare/v0.3.1...v0.3.2)</small>

### Bug Fixes
- Repeated range ([8d49c91](https://github.com/williamfzc/stagesepx/commit/8d49c9127aab4764e12cfa8d0338cdb7e4afd083) by williamfzc).
- Wrong video path ([2c1bdbe](https://github.com/williamfzc/stagesepx/commit/2c1bdbe0b8e14b7d8c32df8de0fbd8202359e801) by williamfzc).

### Features
- Custom content in report ([7c1ec71](https://github.com/williamfzc/stagesepx/commit/7c1ec718344fba23dccdbb9d0db779d0444a0515) by williamfzc).


## [v0.3.1](https://github.com/williamfzc/stagesepx/releases/tag/v0.3.1) - 2019-07-26

<small>[Compare with v0.3.0](https://github.com/williamfzc/stagesepx/compare/v0.3.0...v0.3.1)</small>

### Bug Fixes
- Always drop last range before ([d50d91e](https://github.com/williamfzc/stagesepx/commit/d50d91e6161cd9981c1a639c67f29d68ab2638e0) by williamfzc).
- When length == 1, start > end ([d62d402](https://github.com/williamfzc/stagesepx/commit/d62d4027631e1d9a02c8fb4058aee1165760813e) by williamfzc).
- Put html content in script ([4327b17](https://github.com/williamfzc/stagesepx/commit/4327b1749724e480111e532a5d9b797dd4af1261) by williamfzc).
- Include .html file in setup.py ([9a45366](https://github.com/williamfzc/stagesepx/commit/9a45366596a6b6be6de75a7277e05675bbbd918f) by williamfzc).

### Features
- Better report with bootstrap4 ([b10104d](https://github.com/williamfzc/stagesepx/commit/b10104dbed94b706f40c63ef01a0d6047bf461a5) by williamfzc).


## [v0.3.0](https://github.com/williamfzc/stagesepx/releases/tag/v0.3.0) - 2019-07-25

<small>[Compare with v0.2.1](https://github.com/williamfzc/stagesepx/compare/v0.2.1...v0.3.0)</small>

### Bug Fixes
- Remove intersection between stable and unstable ([91ad621](https://github.com/williamfzc/stagesepx/commit/91ad6213d7c501c0eed281cff7554df20752513b) by williamfzc).
- Relationship between frame id and actual frame ([74da7c1](https://github.com/williamfzc/stagesepx/commit/74da7c1500c4a5782943ec719c4df1e26230fd4b) by williamfzc).

### Features
- Support inserting thumbnail into report ([fe9a0e3](https://github.com/williamfzc/stagesepx/commit/fe9a0e3e3a8230466b0ca1b0adb12b7758ba2b88) by williamfzc).
- Support saving thumbnail to file ([7df155c](https://github.com/williamfzc/stagesepx/commit/7df155cfb5869fefb9e9d7fe667ec5b85cae3c8c) by williamfzc).
- Thumbnail for stage ([6761ff5](https://github.com/williamfzc/stagesepx/commit/6761ff5960121d06800a1953e20bc521600164f3) by williamfzc).
- Add example ([97ceeb9](https://github.com/williamfzc/stagesepx/commit/97ceeb9fd6c198fd524722797497af90a408f8db) by williamfzc).
- Support loading range as data directly ([7ff66f5](https://github.com/williamfzc/stagesepx/commit/7ff66f571caaeb22e278ee0a125e7d29a97e0e18) by williamfzc).


## [v0.2.1](https://github.com/williamfzc/stagesepx/releases/tag/v0.2.1) - 2019-07-22

<small>[Compare with v0.2.0](https://github.com/williamfzc/stagesepx/compare/v0.2.0...v0.2.1)</small>

### Features
- Support threshold in getting stable (and unstable) range ([70afa81](https://github.com/williamfzc/stagesepx/commit/70afa81a16eba17de29ea075056877fe110bb622) by williamfzc).


## [v0.2.0](https://github.com/williamfzc/stagesepx/releases/tag/v0.2.0) - 2019-07-22

<small>[Compare with v0.1.0](https://github.com/williamfzc/stagesepx/compare/v0.1.0...v0.2.0)</small>

### Bug Fixes
- Use abs path of picture ([32b166a](https://github.com/williamfzc/stagesepx/commit/32b166afee556082d606838b7917457c13c1ebb7) by williamfzc).
- Remove un-runnable code ([12eb5f6](https://github.com/williamfzc/stagesepx/commit/12eb5f616ddb28a044aba6c28a1b5eb21a9b0200) by williamfzc).
- Lost last frame ([09f1936](https://github.com/williamfzc/stagesepx/commit/09f1936b5d87a4381e7574da1c3a90a513013534) by williamfzc).
- Calculation of time cost ([db54b84](https://github.com/williamfzc/stagesepx/commit/db54b84ce796c3d53d2d01b50a7bd2623c60c372) by williamfzc).
- Rename 'none' to 'raw' ([4586826](https://github.com/williamfzc/stagesepx/commit/45868266ebbde14623fe91be27bdf1e29b4b5ecc) by williamfzc).

### Code Refactoring
- Duplicate code in classifiers ([3f96e73](https://github.com/williamfzc/stagesepx/commit/3f96e7300b68cb18e3fd79f1e60acf7271a7dc75) by williamfzc).
- Split different classifiers ([595d051](https://github.com/williamfzc/stagesepx/commit/595d0511cf4308d15425e392d01eb33748ca65cd) by williamfzc).

### Features
- Better reporter ([985377d](https://github.com/williamfzc/stagesepx/commit/985377d2348b965da802d4d118dd0359366b2574) by williamfzc).
- Support 'step' in classify ([d828b40](https://github.com/williamfzc/stagesepx/commit/d828b401a949b026ec696b98cf6c86149e3de23a) by williamfzc).
- Support findit ([eec0f25](https://github.com/williamfzc/stagesepx/commit/eec0f253f013c230ce004c096e6bca49a0e32f7d) by williamfzc).
- Support limit range ([3b37623](https://github.com/williamfzc/stagesepx/commit/3b37623ed53b4e89b776b84ea8a17c1dc1114ef1) by williamfzc).
- Support feature extraction ([cacecff](https://github.com/williamfzc/stagesepx/commit/cacecff53d4b8eeac7bc142b7f8509668dd8f348) by williamfzc).


## [v0.1.0](https://github.com/williamfzc/stagesepx/releases/tag/v0.1.0) - 2019-07-17

<small>[Compare with first commit](https://github.com/williamfzc/stagesepx/compare/6864e8ed2fbbf8efb7b2101e89dd7e55d5f70082...v0.1.0)</small>

### Bug Fixes
- Calculation based on all pictures, not one of them ([4fc99c4](https://github.com/williamfzc/stagesepx/commit/4fc99c47830119498dcd39f4845bfee6cdfa6475) by williamfzc).
- Syntax issue ([f7fbae2](https://github.com/williamfzc/stagesepx/commit/f7fbae25a687004bd834300253a7d44a33c15f96) by williamfzc).

### Features
- Import and export for model ([51f89e1](https://github.com/williamfzc/stagesepx/commit/51f89e13acef49636af08def24361e49190fdf3a) by williamfzc).
- Better chart ([6bbb46a](https://github.com/williamfzc/stagesepx/commit/6bbb46a577996eb1826de0c03666bdaf28c3205b) by williamfzc).
- Svm classifier (not precise enough now) ([39a214c](https://github.com/williamfzc/stagesepx/commit/39a214ca4744f0d508c1ee3891e3d9a5444f1321) by williamfzc).
- Chart improvement ([31dedc0](https://github.com/williamfzc/stagesepx/commit/31dedc01a85093c9a630ccb1d8bc84d512979304) by williamfzc).
- Length filter ([6b00efb](https://github.com/williamfzc/stagesepx/commit/6b00efbfd747fa3e8f07b804d8b6c51efd42f9cd) by williamfzc).
- Reporter ([6e56bc6](https://github.com/williamfzc/stagesepx/commit/6e56bc69f8b73e8674c1f95cd0ff3057553774bc) by williamfzc).
- Classify ([bcbdabb](https://github.com/williamfzc/stagesepx/commit/bcbdabb4ec1d8ca2ea37837834e66108b903f20a) by williamfzc).
- Cutter ([a238a0d](https://github.com/williamfzc/stagesepx/commit/a238a0d097d91ddbf64c204640b6f9a0dd8c9d39) by williamfzc).
- Cutter (base) ([d2b610a](https://github.com/williamfzc/stagesepx/commit/d2b610a41c5a4f5466e8d063377390ece25d1204) by williamfzc).


