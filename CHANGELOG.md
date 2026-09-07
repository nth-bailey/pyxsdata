# [1.3.0](https://github.com/nth-bailey/pyxsdata/compare/1.2.2...1.3.0) (2026-09-07)


### Features

* implement StrEnum support, schema default metadata, and root mismatch validation ([ea3db10](https://github.com/nth-bailey/pyxsdata/commit/ea3db1025658c45f235ee113b5ea674d02dfdfa9)), closes [#1223](https://github.com/nth-bailey/pyxsdata/issues/1223) [#1184](https://github.com/nth-bailey/pyxsdata/issues/1184) [#1141](https://github.com/nth-bailey/pyxsdata/issues/1141)

## [1.2.2](https://github.com/nth-bailey/pyxsdata/compare/1.2.1...1.2.2) (2026-09-07)


### Bug Fixes

* resolve upstream xsdata bugs for XXE, NewType, choice subclasses, and SOAP client headers ([3005cb2](https://github.com/nth-bailey/pyxsdata/commit/3005cb2f160655a0e53bdb1e31f29b92c481cac4))

## [1.2.1](https://github.com/nth-bailey/pyxsdata/compare/1.2.0...1.2.1) (2026-09-07)


### Bug Fixes

* **codegen:** remove redundant truthy check on tuple to satisfy ty ([9598f09](https://github.com/nth-bailey/pyxsdata/commit/9598f0974d4103c82c0022c1036fa30590200cec))

# [1.2.0](https://github.com/nth-bailey/pyxsdata/compare/1.1.1...1.2.0) (2026-09-07)


### Features

* **pydantic:** map XSD restrictions to native Pydantic v2 field constraints and use frozen=True ([c821ada](https://github.com/nth-bailey/pyxsdata/commit/c821ada24ffb4e770abd33f004916f0786d9db80))

## [1.1.1](https://github.com/nth-bailey/pyxsdata/compare/1.1.0...1.1.1) (2026-09-07)


### Bug Fixes

* **pydantic:** resolve duplicate default on prohibited fields, instance model_fields access, and add field overloads ([74aff56](https://github.com/nth-bailey/pyxsdata/commit/74aff56339590316fc37b15d18924ef1a55f33d5))

# [1.1.0](https://github.com/nth-bailey/pyxsdata/compare/1.0.3...1.1.0) (2026-09-07)


### Bug Fixes

* **packaging:** keep core extra decoupled from all to avoid PyPI resolution in pure-python environments ([ebac0c2](https://github.com/nth-bailey/pyxsdata/commit/ebac0c2aa8fab778c4bf53b4e4779db3caeedc15))


### Features

* **parsers:** add CoreEventHandler and CoreXmlParser for pyxsdata-core acceleration ([28c6ff3](https://github.com/nth-bailey/pyxsdata/commit/28c6ff3816f43241ef7c4470078e3ce5c5dd0eaf))
* **pydantic:** add CoreXmlParser powered by pyxsdata-core acceleration ([7652331](https://github.com/nth-bailey/pyxsdata/commit/7652331c5514973eaf7fe02db8cbf8d6b0a42f20))

## [1.0.3](https://github.com/nth-bailey/pyxsdata/compare/1.0.2...1.0.3) (2026-09-07)


### Performance Improvements

* **parsers:** direct scalar/proxy converter fast paths and tuple child iteration ([90098e6](https://github.com/nth-bailey/pyxsdata/commit/90098e681e14426d615d0092967272c9091c5cd6))

## [1.0.2](https://github.com/nth-bailey/pyxsdata/compare/1.0.1...1.0.2) (2026-09-07)


### Performance Improvements

* **parsers:** cache child metadata lookups, fast-path primitive nodes, and eliminate object slicing ([da8f091](https://github.com/nth-bailey/pyxsdata/commit/da8f091f8b5df3be3179e5db0f09e479dcfc0737))

## [1.0.1](https://github.com/nth-bailey/pyxsdata/compare/1.0.0...1.0.1) (2026-09-07)


### Performance Improvements

* **parsers:** optimize XML deserialization pipeline and document performance gains vs xsdata ([088842d](https://github.com/nth-bailey/pyxsdata/commit/088842deb65da87483c466adbe6dc9b63185932c))

# 1.0.0 (2026-09-07)


### Bug Fixes

* All non-native types must have a reference id ([5ca49de](https://github.com/nth-bailey/pyxsdata/commit/5ca49de4f3c04ea0a7d3bb4e482b69975a2066a5))
* Allow soap client config subclassing ([#1010](https://github.com/nth-bailey/pyxsdata/issues/1010)) ([9be40c4](https://github.com/nth-bailey/pyxsdata/commit/9be40c4916d6155eea1682cc799b0d99cf4454fc)), closes [#1009](https://github.com/nth-bailey/pyxsdata/issues/1009)
* Always keep forward references for choice types ([cfd72d3](https://github.com/nth-bailey/pyxsdata/commit/cfd72d39080294abcbc6b332193fff5bca55e96b)), closes [#882](https://github.com/nth-bailey/pyxsdata/issues/882)
* Avoid conflict with attributes named value when flattening extensions ([#1085](https://github.com/nth-bailey/pyxsdata/issues/1085)) ([827210b](https://github.com/nth-bailey/pyxsdata/commit/827210be0df1be7e8081d39a6e5a14c750deaa89))
* Avoid recursive error on nested group references ([00fe560](https://github.com/nth-bailey/pyxsdata/commit/00fe560b2ff26de2d2b2c71d40ac074046aa5065))
* Avoid using not-threadsafe arnings.catch_warning ([#1042](https://github.com/nth-bailey/pyxsdata/issues/1042)) ([ff5e759](https://github.com/nth-bailey/pyxsdata/commit/ff5e7593361115be95a21d7d9ee0049be440f6b0))
* broken doctest ([#1026](https://github.com/nth-bailey/pyxsdata/issues/1026)) ([eab6bb7](https://github.com/nth-bailey/pyxsdata/commit/eab6bb7b0a31dbc5cf31c894d9f9c6640bbc27e0))
* **ci:** fix step order, concurrency, and action versions in docs.yml ([8ebaae0](https://github.com/nth-bailey/pyxsdata/commit/8ebaae05cc27a3e1ffcc7d09bd2af8c7d5a0fa32))
* Conflicting enum values leads to wrong default values ([#806](https://github.com/nth-bailey/pyxsdata/issues/806)) ([c72c4cd](https://github.com/nth-bailey/pyxsdata/commit/c72c4cd137305372e19c7b8dec425fa1cc7f36b9))
* Derived element json serialization ([#1035](https://github.com/nth-bailey/pyxsdata/issues/1035)) ([f4b6965](https://github.com/nth-bailey/pyxsdata/commit/f4b6965f9accfb311371c667eac4f53ca5f989c3))
* Dict mapper to recognize optional attrs ([f6eaa8f](https://github.com/nth-bailey/pyxsdata/commit/f6eaa8f49603fcf3174e8f06abf456dbe88ae4be))
* **docs:** fix typo on type `str` ([#1021](https://github.com/nth-bailey/pyxsdata/issues/1021)) ([fcf7f33](https://github.com/nth-bailey/pyxsdata/commit/fcf7f33bc41dae69e9aeff62adf1b29cee8a3ffd))
* Encode attrs in tree serializer ([#1023](https://github.com/nth-bailey/pyxsdata/issues/1023)) ([a2af584](https://github.com/nth-bailey/pyxsdata/commit/a2af58409cd5858c33a280d57c17585d95ca73eb))
* Encode data in tree serializer ([#1022](https://github.com/nth-bailey/pyxsdata/issues/1022)) ([0e4d2b5](https://github.com/nth-bailey/pyxsdata/commit/0e4d2b56677978696417620ae1f8d828f46362d2))
* Ensure original name case returns valid python identifiers ([#950](https://github.com/nth-bailey/pyxsdata/issues/950)) ([853bb04](https://github.com/nth-bailey/pyxsdata/commit/853bb0482e5ded5df3d9cd6818dcdcd705616ef6))
* **formats:** use inspect module to gather annotations ([#1173](https://github.com/nth-bailey/pyxsdata/issues/1173)) ([28f63e8](https://github.com/nth-bailey/pyxsdata/commit/28f63e8ffe912341e5622dfb7c0973d920c1fd05))
* Generate type hints for compound fields with token elements ([#997](https://github.com/nth-bailey/pyxsdata/issues/997)) ([ff01d9b](https://github.com/nth-bailey/pyxsdata/commit/ff01d9b225c49e287c5979555ca419b4f8bae32d))
* Improve downloader to handle all schemas structures ([#1199](https://github.com/nth-bailey/pyxsdata/issues/1199)) ([fa89208](https://github.com/nth-bailey/pyxsdata/commit/fa89208ddbc007499c950f1c1fa43b1cbea4f14b))
* Maintain compound field types ordering ([#885](https://github.com/nth-bailey/pyxsdata/issues/885)) ([db9c34b](https://github.com/nth-bailey/pyxsdata/commit/db9c34b5e55871c065c3506c00e3edd9137c5120))
* Mark body and fault as optional in output soap classes ([#1099](https://github.com/nth-bailey/pyxsdata/issues/1099)) ([cd707c8](https://github.com/nth-bailey/pyxsdata/commit/cd707c8638d9e8561b30704e2c225bec87f030ce))
* Move ruff format in the code generator ([fbaebf5](https://github.com/nth-bailey/pyxsdata/commit/fbaebf545628e6e24d73c86cbc8590cb094bb779))
* mypy issues ([7490c77](https://github.com/nth-bailey/pyxsdata/commit/7490c7724372d2cf1fc50d13bda385de4f87abd8))
* Prohibited fields need default value None ([#1098](https://github.com/nth-bailey/pyxsdata/issues/1098)) ([95755fe](https://github.com/nth-bailey/pyxsdata/commit/95755fe11e253b38ee1df5112880a0529203a15f)), closes [#1091](https://github.com/nth-bailey/pyxsdata/issues/1091)
* Protect prohibitted attrs from turning into lists ([0bc0da3](https://github.com/nth-bailey/pyxsdata/commit/0bc0da3d20d5001aaf7f8f8be7cab48ae13bdda0))
* **pydantic:** support JSON schema generation for XML data types ([#41](https://github.com/nth-bailey/pyxsdata/issues/41)) ([35edb26](https://github.com/nth-bailey/pyxsdata/commit/35edb2699c7d451704fc761ae3643f8a63d61fff))
* Python 3.13 deprecation ([#1077](https://github.com/nth-bailey/pyxsdata/issues/1077)) ([9a0e785](https://github.com/nth-bailey/pyxsdata/commit/9a0e785a175a1f263da45262209c79b0eced0ace))
* Renaming classes assigns wrong references ([#967](https://github.com/nth-bailey/pyxsdata/issues/967)) ([c94cbb7](https://github.com/nth-bailey/pyxsdata/commit/c94cbb7eaff228a80be8b98d0b9600b39a0a1cbc))
* Resolve attr name collisions with unusual names ([#991](https://github.com/nth-bailey/pyxsdata/issues/991)) ([6820aa1](https://github.com/nth-bailey/pyxsdata/commit/6820aa1dc8ffd15a486dd2d845ff76cde4511db9))
* resolve minimal installation hook loading and python 3.14 bytecode coverage ([6df5805](https://github.com/nth-bailey/pyxsdata/commit/6df58052b8190d9650a70e8960604127ce351510))
* Resolve xml meta var index conflicts ([d38e229](https://github.com/nth-bailey/pyxsdata/commit/d38e229607214244d8cf6d5944d913efa610deba))
* Respect encoding configuration in lxml event writer ([#940](https://github.com/nth-bailey/pyxsdata/issues/940)) ([d1844e3](https://github.com/nth-bailey/pyxsdata/commit/d1844e3649779f1a5a6c0edf7aab5318b17c9d54)), closes [#923](https://github.com/nth-bailey/pyxsdata/issues/923)
* Ruff check command typo breaks generator ([#1061](https://github.com/nth-bailey/pyxsdata/issues/1061)) ([3ad50f2](https://github.com/nth-bailey/pyxsdata/commit/3ad50f2d9bcdeeed3162f6a4746c801d8ad89616))
* Run Ruff on package directories rather than files ([#1049](https://github.com/nth-bailey/pyxsdata/issues/1049)) ([791a98e](https://github.com/nth-bailey/pyxsdata/commit/791a98e554b35bb5618aa07971c0f88a5667f0b2))
* Support mixed content for DTD elements ([#749](https://github.com/nth-bailey/pyxsdata/issues/749)) ([28dea68](https://github.com/nth-bailey/pyxsdata/commit/28dea6840ba29c6a7c5d36b1c3340fe2b0798656))
* TreeSerializer start pending tag on all flush events" ([#1025](https://github.com/nth-bailey/pyxsdata/issues/1025)) ([826e6f2](https://github.com/nth-bailey/pyxsdata/commit/826e6f285baf1ee0791473c818889f58167378c7))
* unnest class with circular reference ([2604d8b](https://github.com/nth-bailey/pyxsdata/commit/2604d8b127214543e6744af3480d4e325a4589c3))
* Unnest classes should update inner classes recursively ([c022af6](https://github.com/nth-bailey/pyxsdata/commit/c022af664f1e2498d549cca8b798cc7c0e40d1af))
* Use ruff to enforce double quotes on patterns ([bf986e4](https://github.com/nth-bailey/pyxsdata/commit/bf986e402f320a9de688e70c617416b05f39cd61))
* Validate min < max occurs ([#979](https://github.com/nth-bailey/pyxsdata/issues/979)) ([d4566b4](https://github.com/nth-bailey/pyxsdata/commit/d4566b45774cf2305a7b38cc9913116abda0a6fc))


### Features

* Add abstract suffixes to resolve class name conflicts ([#985](https://github.com/nth-bailey/pyxsdata/issues/985)) ([b43b9c7](https://github.com/nth-bailey/pyxsdata/commit/b43b9c77b67db2713e2afb0a9f466aff4ff46027))
* Add class and field info in parsing validation warnings ([#1036](https://github.com/nth-bailey/pyxsdata/issues/1036)) ([d561ff5](https://github.com/nth-bailey/pyxsdata/commit/d561ff558ede1eb066823858f3addc5b3a392f64))
* Add cli info header ([885ef84](https://github.com/nth-bailey/pyxsdata/commit/885ef84cf8db30ea6eae6a862e8375ab92f71e93))
* Add codegen debug messages with performance stats ([ce27182](https://github.com/nth-bailey/pyxsdata/commit/ce27182ea31be70631c31f01f2f9af8265b94772))
* Add codegen handler to disambiguate choices ([745d2f7](https://github.com/nth-bailey/pyxsdata/commit/745d2f7148b850bf67483e8eda9aebdecdce44e0))
* Add config to generate wrapper fields ([9eae7f9](https://github.com/nth-bailey/pyxsdata/commit/9eae7f9afe3765b1020519e5f60a7477b3cf9682))
* Add generator output config include header ([3a65aec](https://github.com/nth-bailey/pyxsdata/commit/3a65aec178baf54c231bed8f63c81d058c754a45))
* Add handler to generate wrapper fields ([7cfc3af](https://github.com/nth-bailey/pyxsdata/commit/7cfc3afaf9b8b4abf16a16933063a44c60651b79))
* Add option to ignore xml pattern restrictions ([8114c4d](https://github.com/nth-bailey/pyxsdata/commit/8114c4d9f8b5ef3e9e56e0a31a593715ce4e11b6))
* Add src code excerpt on ruff errors ([#996](https://github.com/nth-bailey/pyxsdata/issues/996)) ([a15c3e7](https://github.com/nth-bailey/pyxsdata/commit/a15c3e7d8827fa5382a2e005a325ea29c8aa2a3c))
* Add warning for same module designation ([#1018](https://github.com/nth-bailey/pyxsdata/issues/1018)) ([c4674f6](https://github.com/nth-bailey/pyxsdata/commit/c4674f67d38029a8908e20e518f2aae186264c38))
* Add xml and lxml tree serializers ([d0e2d56](https://github.com/nth-bailey/pyxsdata/commit/d0e2d56b12e096596087958795ac5cda8da7341d)), closes [#849](https://github.com/nth-bailey/pyxsdata/issues/849)
* Add xsdata version in the cli cache key ([#990](https://github.com/nth-bailey/pyxsdata/issues/990)) ([27c62e6](https://github.com/nth-bailey/pyxsdata/commit/27c62e6ff6915a97384fb661c2edf0db2f4f88cf))
* Allow config substitutions to specify re replace strings ([#755](https://github.com/nth-bailey/pyxsdata/issues/755)) ([7497f0a](https://github.com/nth-bailey/pyxsdata/commit/7497f0a9948c089895d207f8dcbb7511e8754380))
* Allow generators as array elements ([#1074](https://github.com/nth-bailey/pyxsdata/issues/1074)) ([cff2df1](https://github.com/nth-bailey/pyxsdata/commit/cff2df1202ce8252eb2f9d6f7858f8e69e5f856f))
* Avoid generating same classes ([3eebc37](https://github.com/nth-bailey/pyxsdata/commit/3eebc3730cfc2acf7c33a61c226865dd064001ee))
* Capture namespace prefixes in user dicts ([#978](https://github.com/nth-bailey/pyxsdata/issues/978)) ([93a8ca0](https://github.com/nth-bailey/pyxsdata/commit/93a8ca0548d1f7badb628ad9fd0327672abe140b)), closes [#847](https://github.com/nth-bailey/pyxsdata/issues/847)
* Convert child attr to list when parent is list ([ffe2bd1](https://github.com/nth-bailey/pyxsdata/commit/ffe2bd1c26482b183234cf4fc6e3f9fd3c9ea580))
* Detect and alert circular imports ([#999](https://github.com/nth-bailey/pyxsdata/issues/999)) ([6441877](https://github.com/nth-bailey/pyxsdata/commit/644187724e18e42cb4c853c2358620fa43030923))
* Detect circular references more accurately ([#969](https://github.com/nth-bailey/pyxsdata/issues/969)) ([b8a2abc](https://github.com/nth-bailey/pyxsdata/commit/b8a2abcbc617ea67c5d49a756d645cf12964a16c))
* Extract event generator from XmlSerializer ([6bbc299](https://github.com/nth-bailey/pyxsdata/commit/6bbc2993397be9c53bfa8e0b3c1a4466b7082a75))
* Filter element unions against fixed attribute values ([#1066](https://github.com/nth-bailey/pyxsdata/issues/1066)) ([6eccffb](https://github.com/nth-bailey/pyxsdata/commit/6eccffb886ca537c4d1b1fa0f59cac637311e43f))
* Generate combound fields for non-list elements ([97b646d](https://github.com/nth-bailey/pyxsdata/commit/97b646d91cfdb9c9c28a54c7f89466e251375e48))
* Generate compound field choices max occurs ([#994](https://github.com/nth-bailey/pyxsdata/issues/994)) ([cd65e54](https://github.com/nth-bailey/pyxsdata/commit/cd65e54b2a66db6ec963fc33d0fe0923aa793c6b)), closes [#742](https://github.com/nth-bailey/pyxsdata/issues/742)
* Generate ForwardRef() instead of Type[] ([762ecb8](https://github.com/nth-bailey/pyxsdata/commit/762ecb837a541adf4ea377a0c1223eacd5008a95))
* Generate wrapper fields for forward references ([45f8a06](https://github.com/nth-bailey/pyxsdata/commit/45f8a06c55500cd860ea33be54d700205ad78798))
* Ignore malformed json files in transformer ([#750](https://github.com/nth-bailey/pyxsdata/issues/750)) ([a73385b](https://github.com/nth-bailey/pyxsdata/commit/a73385b36598f69fe4291952801079d36678c028))
* Implement Tree serializer v2 ([510b2b9](https://github.com/nth-bailey/pyxsdata/commit/510b2b93051203e76f9bc3770784c386879c2302))
* Improve codegen errors ([#970](https://github.com/nth-bailey/pyxsdata/issues/970)) ([77c05ef](https://github.com/nth-bailey/pyxsdata/commit/77c05ef76d4fa31ef9bfe9208835bd4a6bdb3b62))
* Include common soap encoding schema ([#1100](https://github.com/nth-bailey/pyxsdata/issues/1100)) ([ab4dc9c](https://github.com/nth-bailey/pyxsdata/commit/ab4dc9cc2834c4375402f9d811af2600810325ab))
* Make rename duplicate attributes reusable ([#984](https://github.com/nth-bailey/pyxsdata/issues/984)) ([fb6a692](https://github.com/nth-bailey/pyxsdata/commit/fb6a692bf67a4294502969fa694533e66f88cfc2))
* modernize to pyxsdata 26.3.0 ([f0d6173](https://github.com/nth-bailey/pyxsdata/commit/f0d617376778075fd19ee13d691e7c38977b43f6))
* Move analyzer validations to handler ([ae00dd0](https://github.com/nth-bailey/pyxsdata/commit/ae00dd0fdd2d62474b146a36ac590e5c12637650))
* Navigate from inner to outer classes ([b6afc78](https://github.com/nth-bailey/pyxsdata/commit/b6afc789fbe7bf23a43742f1bf480bb50d188710))
* **parsers:** add pugixml event handler and optional dependency extra ([4d154b7](https://github.com/nth-bailey/pyxsdata/commit/4d154b7707d281ebb34034976d0050e09c27c65a))
* Prevent classes with ambiguous choices ([106b710](https://github.com/nth-bailey/pyxsdata/commit/106b7101156b960e0563168972676d84bbd024e3))
* Relax float inf/nan strict matching ([e08390a](https://github.com/nth-bailey/pyxsdata/commit/e08390ae62f97e168f0a8c538a5b93bf6b08cf05))
* **release:** configure semantic-release with PyPI publishing and overhaul docs ([89a8df2](https://github.com/nth-bailey/pyxsdata/commit/89a8df2478e69211b5f9c71cbd3427bb401444db))
* Remove whitespace from bytes encoded xml strings ([#1037](https://github.com/nth-bailey/pyxsdata/issues/1037)) ([3713c6a](https://github.com/nth-bailey/pyxsdata/commit/3713c6a091d8637c27203b820ff99b3e833dba03))
* Rewrite types analyze process ([875ef19](https://github.com/nth-bailey/pyxsdata/commit/875ef19dd5bb5b73aeb77593721068b725a4508f))
* Stop flattening complex types ([a06733b](https://github.com/nth-bailey/pyxsdata/commit/a06733b1ac407f8bb210d63d52d372d6f74bacc1))
* Support wrapper fields in json parser/serializer ([68308b7](https://github.com/nth-bailey/pyxsdata/commit/68308b7731fa7d2d833110db2863896fd66d4e24))
* Update ruff min version ([24a8fa9](https://github.com/nth-bailey/pyxsdata/commit/24a8fa9282b1c3cb0387a27529aa01e0048968c0))
* Use bidirectional classes navigation in filters ([21e09ce](https://github.com/nth-bailey/pyxsdata/commit/21e09ce776b3f984a688b1588db09b8cce38a434))
* Use deepcopy to clone codegen models ([#980](https://github.com/nth-bailey/pyxsdata/issues/980)) ([6030317](https://github.com/nth-bailey/pyxsdata/commit/6030317d04449302ee4c5d5ca02ddababbd1568a))
* Use ruff isort during codegen ([#972](https://github.com/nth-bailey/pyxsdata/issues/972)) ([d836d8b](https://github.com/nth-bailey/pyxsdata/commit/d836d8bc121797f6adcf583d2d9847795172b7d6))
* Use unicodedata.name on non-alphanumeric attr names ([#993](https://github.com/nth-bailey/pyxsdata/issues/993)) ([e652e08](https://github.com/nth-bailey/pyxsdata/commit/e652e08c2fc312f85cc35e4f6b0c8c3948b9d071))
* Validate fixed values ([73ddc8c](https://github.com/nth-bailey/pyxsdata/commit/73ddc8c23c756e8e489950694c890b8b177df250))
* XmlSerializer skip optional nillable elements ([#1067](https://github.com/nth-bailey/pyxsdata/issues/1067)) ([2d4c5bf](https://github.com/nth-bailey/pyxsdata/commit/2d4c5bfed2d513c2ca622d91da8fa6e80646e5dd))


### Performance Improvements

* Run ruff commands once ([2c56e93](https://github.com/nth-bailey/pyxsdata/commit/2c56e937c0dd42d2e678ec44d2e4a6b540faa261))
* Update all class references in one pass ([#987](https://github.com/nth-bailey/pyxsdata/issues/987)) ([8608f7f](https://github.com/nth-bailey/pyxsdata/commit/8608f7f433bc9cf7fec8af674f8619797b834694))


### Reverts

* Add back support for optional lists ([#1053](https://github.com/nth-bailey/pyxsdata/issues/1053)) ([1f42a6a](https://github.com/nth-bailey/pyxsdata/commit/1f42a6a5990664494049d4f97810cb0bcccc76df))

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added `PugixmlEventHandler` powered by `pygixml` (Cython streaming wrapper around
  pugixml + yxml) for ultra-fast, constant-memory XML pull-parsing.
- Added `pugixml` optional dependency extra (`pip install "pyxsdata[pugixml]"`).
- Integrated `PugixmlEventHandler` into performance benchmark suite.

## [0.0.0] - 2026-03-07

### Added

- Native Pydantic v2 support (`pyxsdata.pydantic`) with drop-in parsers and serializers
  (`XmlParser`, `XmlSerializer`, `JsonParser`, etc.).
- Dedicated Pydantic v2 code generation backend
  (`pyxsdata generate ... --output pydantic`).
- Astral `ty` static type checker integration with zero diagnostics.
- Modern documentation website powered by Zensical static site generator.
- Automated GitHub Pages documentation deployment workflow using Zensical.

### Fixed

- Fixed Pydantic `model_json_schema()` generation failing on models containing internal
  XML data types (`XmlDate`, `XmlDateTime`, `XmlTime`, `XmlDuration`, `XmlPeriod`,
  `QName`).

### Changed

- Forked and rebranded library strictly to `pyxsdata`.
- Raised minimum required Python version to `>= 3.12`.
- Modernized codebase to PEP 695 generics, modern type unions, and structural pattern
  matching.
- Upgraded all core and optional dependencies to latest releases.
- Migrated linter and type checker configurations to standalone `ruff.toml` and
  `ty.toml`, enforcing Google Python Style Guide conventions.

### Removed

- Dropped legacy `xsdata` CLI command and backward-compatibility aliases.
- Removed `mypy` and `mkdocs` toolchains, hooks, and legacy documentation
  configurations.

---

## Legacy xsdata History

<details>
<summary>Click to expand historical changelog from upstream xsdata (v26.2 and older)</summary>

## 26.2 (2026-02-15)

**Fixes**

- Fix elements in same choice different branches incorrectly merged as list
  ([#1206](https://github.com/tefra/xsdata/pull/1206))

**Features**

- Infer XML required property from typing annotations
  ([#1208](https://github.com/tefra/xsdata/pull/1208))
- Generate required metadata only for attributes without default values
  ([#1208](https://github.com/tefra/xsdata/pull/1208))

## 26.1 (2026-01-20)

**Fixes**

- Fixed missing imports on inheriting multiple mixins for the same class
  ([#1156](https://github.com/tefra/xsdata/pull/1156))
- Fixed choice elements with minOccurs <= 1 not marked as optional
- Fixed incorrect max_occurs for elements in different choice blocks
  ([#1179](https://github.com/tefra/xsdata/pull/1179))
- Fixed AttributeError when retrieving subclasses from cython packages
  ([#1200](https://github.com/tefra/xsdata/pull/1200))

**Features**

- Added flag for specifying extensions
  ([#1168](https://github.com/tefra/xsdata/pull/1168))
- Added support for python 3.14 ([#1173](https://github.com/tefra/xsdata/pull/1173))
- Switched to Sequence when using generic containers
  ([#1201](https://github.com/tefra/xsdata/pull/1201))

**Deprecations**

- Removed Python 3.9 support ([#1189](https://github.com/tefra/xsdata/pull/1189))
  ([#1191](https://github.com/tefra/xsdata/pull/1191))
- Removed cli options union-type, kw-only, postponed-annotations are now always enabled
- Removed xsdata <SOURCE> shorthand ([#1128](https://github.com/tefra/xsdata/pull/1128))

## 25.7 (2025-07-06)

**Fixes**

- Ignore dynamic classes in auto-discovery mode.
  ([#1144](https://github.com/tefra/xsdata/pull/1144))
- Parsing tail content with nested mixed classes
  ([#1151](https://github.com/tefra/xsdata/pull/1151))

## 25.4 (2025-04-13)

**Features**

- Allow extensions to match module paths
  ([#1132](https://github.com/tefra/xsdata/pull/1132))

- Improve duplicate class names detection and resolution
  ([#1127](https://github.com/tefra/xsdata/pull/1127))

**Fixes**

- Resolve Code Quality Issue

## 24.12 (2024-12-22)

**Fixes**

- Set the default value of prohibited fields to None
  ([#1098](https://github.com/tefra/xsdata/pull/1098))

- Set body and fault as optional in output soap classes
  ([#1099](https://github.com/tefra/xsdata/pull/1099))

- Resolve a conflict with type location when an element and a complex type have the same
  name ([#1107](https://github.com/tefra/xsdata/pull/1107))

**Features**

- Allow Xml Parser subclasses to override how the root class is located
  ([#1090](https://github.com/tefra/xsdata/pull/1090))

- Include common soap encoding schema
  ([#1100](https://github.com/tefra/xsdata/pull/1100))

**Deprecations**

- Remove subscritable types config option
- Remove Type,Tuple,List,Dict from stop words
- Deprecate xsdata <SOURCE> shorthand, use xsdata generate <SOURCE> instead

## 24.11 (2024-11-03)

**Fixes**

- Avoid conflict with attributes named value when flattening extensions
  ([#1085](https://github.com/tefra/xsdata/pull/1085))

**Features**

- Add cli config to use generic collections
  ([#1082](https://github.com/tefra/xsdata/pull/1082))

**Deprecations**

- Drop support for python 3.8

## 24.9 (2024-09-21)

**Fixes**

- Fix typing annotations deprecation warning in Python 3.13
  ([#1077](https://github.com/tefra/xsdata/pull/1077))

**Features**

- Allow generators as array elements
  ([#1074](https://github.com/tefra/xsdata/pull/1074))

## 24.7 (2024-07-28)

**Features**

- Improve XML parsing performance on union elements with fixed attributes
  ([#1066](https://github.com/tefra/xsdata/pull/1066))
- Skip optional and nillable elements on XML Serializer
  ([#1066](https://github.com/tefra/xsdata/pull/1066))

**Fixes**

- Reset attr types derived from missing simple types
  ([#1062](https://github.com/tefra/xsdata/pull/1062))

## 24.6.1 (2024-06-28)

**Fixes**

- Ruff check command typo breaks generator with v0.5.0
  ([#1061](https://github.com/tefra/xsdata/pull/1061))

## 24.6 (2024-06-24)

**Features**

- Add class and field info in parsing warnings
  ([#1036](https://github.com/tefra/xsdata/pull/1036))
- Remove whitespace from bytes encoded xml strings
  ([#1037](https://github.com/tefra/xsdata/pull/1037))
- Improve codegen performance ([#1043](https://github.com/tefra/xsdata/pull/1043))

**Fixes**

- JSON serializer fails on derived elements
  ([#1053](https://github.com/tefra/xsdata/pull/1053))
- Update typing-extensions minimum version
  ([#1039](https://github.com/tefra/xsdata/pull/1039))
- Avoid using not-threadsafe warnings.catch_warning
  ([#1042](https://github.com/tefra/xsdata/pull/1042))
- Unnest classes doesn't update inner classes recursively
  ([#1047](https://github.com/tefra/xsdata/pull/1047))
- Restore support for optional lists
  ([#1053](https://github.com/tefra/xsdata/pull/1053))

## 24.5 (2024-05-07)

**Features**

- Rewrite TreeSerializer, drop support for native python ElementTree
  ([#1032](https://github.com/tefra/xsdata/pull/1032))
- Validate fields fixed values ([#1013](https://github.com/tefra/xsdata/pull/1013))
- Detect optional fields in dict mapper
- Refactor typing annotations analyze process
- Generate ForwardRef() instead of Type[]

**Fixes**

- Allow soap client config subclassing
  ([#1010](https://github.com/tefra/xsdata/pull/1010))
- Avoid recursive error on nested group references
  ([#1016](https://github.com/tefra/xsdata/pull/1016))
- Add warning for same module designation
  ([#1018](https://github.com/tefra/xsdata/pull/1018))

## 24.4 (2024-04-01)

**Features**

- Add xml and lxml tree serializers ([#975](https://github.com/tefra/xsdata/pull/975))
- Capture namespace prefixes in user dicts
  ([#978](https://github.com/tefra/xsdata/pull/978))
- Add cli option to generate wrapper fields
  ([#982](https://github.com/tefra/xsdata/pull/982))
- Support wrapper fields in JSON data bindings
  ([#982](https://github.com/tefra/xsdata/pull/982))
- Use abstract suffixes to resolve class name conflicts
  ([#985](https://github.com/tefra/xsdata/pull/985))
- Add the version number in the cli cache key
  ([#990](https://github.com/tefra/xsdata/pull/990))
- Use unicodedata.name for attrs with only special characters
  ([#993](https://github.com/tefra/xsdata/pull/993))
- Add src code excerpts on ruff errors
  ([#996](https://github.com/tefra/xsdata/pull/996))
- Detect circular imports and raise appropriate error
  ([#999](https://github.com/tefra/xsdata/pull/999))
- Add support for Python 3.13 ([#1001](https://github.com/tefra/xsdata/pull/1001))
- Add cli debug messages with performance stats

**Fixes**

- Use deepcopy to clone codegen models
  ([#980](https://github.com/tefra/xsdata/pull/980))
- Generate type hints for compound fields with token elements
  ([#997](https://github.com/tefra/xsdata/pull/997))
- Protect prohibited attrs from turning into lists
  ([#998](https://github.com/tefra/xsdata/pull/998))
- Convert child attr to list when parent is list
  ([#998](https://github.com/tefra/xsdata/pull/998))

## 24.3.1 (2024-03-10)

**Fixes**

- Unnest class with circular reference
  ([#974](https://github.com/tefra/xsdata/pull/974))

## 24.3 (2024-03-10)

**Features**

- Avoid flattening root elements ([#945](https://github.com/tefra/xsdata/pull/945))
- Avoid generating ambiguous choices ([#946](https://github.com/tefra/xsdata/pull/946))
- Added various type reference validations
  ([#966](https://github.com/tefra/xsdata/pull/966),
  [#967](https://github.com/tefra/xsdata/pull/967),
  [#968](https://github.com/tefra/xsdata/pull/968))
- Calculate circular references more accurately
  ([#969](https://github.com/tefra/xsdata/pull/969))
- Prettify codegen errors ([#970](https://github.com/tefra/xsdata/pull/970))
- Use Ruff to sort imports ([#972](https://github.com/tefra/xsdata/pull/972))

**Fixes**

- Move ruff format in the code generator
  ([#964](https://github.com/tefra/xsdata/pull/964))

## 24.2.1 (2024-02-19)

- Fixed FieldInfo type errors ([#949](https://github.com/tefra/xsdata/pull/949))
- Fixed private package names ([#950](https://github.com/tefra/xsdata/pull/950))

## 24.2 (2024-02-17)

- Added Dict encoder/decoder ([#921](https://github.com/tefra/xsdata/pull/921))
- Deprecated Serializer config pretty_print/pretty_print_indentation
  ([#942](https://github.com/tefra/xsdata/pull/942))
- Fixed lxml event writer to respect the encoding configuration
  ([#940](https://github.com/tefra/xsdata/pull/940))
- Migrated documentation to mkdocs with markdown
- Refactored project docstrings

## 24.1 (2024-01-04)

- Fixed XmlParser to ignore xsi attrs when fail on unknown attributes is enabled
  ([#846](https://github.com/tefra/xsdata/pull/846))
- Fixed parsing mandatory byte elements with no value
  ([#873](https://github.com/tefra/xsdata/pull/873))
- Fixed issue in json binding with union fields
  ([#864](https://github.com/tefra/xsdata/pull/864))
- Fixed PycodeSerializer to escape unicode characters in string values
  ([#877](https://github.com/tefra/xsdata/pull/877))
- Fixed compound field choices with forward references
  ([#886](https://github.com/tefra/xsdata/pull/886))
- Fixed google style docstrings to add missing colon
  ([#884](https://github.com/tefra/xsdata/pull/884))
- Fixed deprecation warnings for datetime.datetime.utcnow()
- Fixed XmlSerializer to ignore empty non-nillable/required tokens
  ([#902](https://github.com/tefra/xsdata/pull/902))
- Fixed issue with invalid variable names when using originalCase naming convention
  ([#881](https://github.com/tefra/xsdata/pull/881))
- Added type hints for compound fields
  ([#858](https://github.com/tefra/xsdata/pull/858),
  [#885](https://github.com/tefra/xsdata/pull/885))
- Added http header when loading remote resources
  ([#867](https://github.com/tefra/xsdata/pull/867))
- Added warning when converting parent field to a list
  ([#871](https://github.com/tefra/xsdata/pull/871))
- Added ruff to format generated code ([#892](https://github.com/tefra/xsdata/pull/892))
- Added option to use substitution group names for compound field name
  ([#905](https://github.com/tefra/xsdata/pull/905))
- Updated base64 decoding to enable validation
  ([#875](https://github.com/tefra/xsdata/pull/875))
- Updated generator to render prohibited parent fields with restriction extensions
  ([#908](https://github.com/tefra/xsdata/pull/908))
- Updated generator so plugins can easily override templates

## 23.8 (2023-08-12)

- Removed Python 3.7 support
- Fixed PycodeSerializer not adding imports for nested classes
- Fixed imports ordering
- Added support for strict content wildcard processing
  ([#803](https://github.com/tefra/xsdata/pull/803))

## 23.7 (2023-07-23)

- Fixed decimal converter to avoid scientific notations
  ([#826](https://github.com/tefra/xsdata/pull/826))
- Fixed nympy parameter docstring format
  ([#827](https://github.com/tefra/xsdata/pull/827))
- Fixed optional/required override validation
  ([#820](https://github.com/tefra/xsdata/pull/820))
- Fixed WSDL mapper to respect the elements original location
  ([#832](https://github.com/tefra/xsdata/pull/832))
- Added Python 3.12 support

## 23.6 (2023-06-24)

- Fixed conflicting enum values leading to wrong default values
  ([#806](https://github.com/tefra/xsdata/pull/806))
- Added support for custom decorators and base classes
  ([#793](https://github.com/tefra/xsdata/pull/793))
- Added parser config to load external dtd to resolve entities
  ([#797](https://github.com/tefra/xsdata/pull/797))
- Added requests sessions on the wsdl client transport
  ([#798](https://github.com/tefra/xsdata/pull/798))
- Added support subscriptable types and UnionType
  ([#801](https://github.com/tefra/xsdata/pull/801))
- Added option to restrict models package for auto-locator
  ([#809](https://github.com/tefra/xsdata/pull/809))
- Updated context to only cache supported classes
  ([#796](https://github.com/tefra/xsdata/pull/796))
- Removed tox requirement ([#800](https://github.com/tefra/xsdata/pull/800))
- Converted to pyproject.toml ([#802](https://github.com/tefra/xsdata/pull/802))

## 23.5 (2023-05-21)

- Fixed XML meta var index conflicts.
- Fixed mixed content handling for DTD elements.
  ([#749](https://github.com/tefra/xsdata/pull/749),
  [#762](https://github.com/tefra/xsdata/pull/762))
- Fixed an issue with required attributes turning into optional ones.
- Fixed calculation of min/max occurs when parsing XML/JSON documents.
  ([#756](https://github.com/tefra/xsdata/pull/756))
- Fixed calculation of min/max occurs when parsing DTD choice content types.
  ([#760](https://github.com/tefra/xsdata/pull/760))
- Fixed an issue when parsing tail content for compound wildcard elements.
- Fixed an issue with the code analyzer not fully processing some classes.
- Fixed an issue with the code analyzer taking forever to process very large
  enumerations. ([#776](https://github.com/tefra/xsdata/issue/776))
- Fixed an issue in the JSON parser with optional choice elements.
- Updated the transformer to silently ignore malformed JSON files.
  ([#750](https://github.com/tefra/xsdata/pull/750))
- Updated the override attribute handler to fix naming conflicts.
- Updated the override attribute handler to allow wildcard overrides.
- Updated conditions on extensions flattening (over-flattening).
  ([#754](https://github.com/tefra/xsdata/pull/754))
- Updated Group, AttributeGroup handling, skipping a few cases.
- Updated how min/max occurs are calculated with nested containers.
- Updated handling of element substitutions to treat them as choices.
  ([#786](https://github.com/tefra/xsdata/pull/786))
- Updated Pycodeserializer to skip default field values.
- Updated flattening restriction base classes when sequence elements are out of order.
- Updated docformatter to v1.6.5.
- Added support to override compound fields.
- Added support for multiple sequential groups in a class.
- Added support for non-list compound fields.
- Added support to mix list and non-list fields with sequence groups.
- Added an option to include headers in generated files.
  ([#746](https://github.com/tefra/xsdata/pull/746))
- Added an option to cache the initial load and mapping of resources.
- Added support for regular expressions in config substitutions.
  ([#755](https://github.com/tefra/xsdata/pull/755))
- Added a pretty print indentation option in the serializer config.
  ([#780](https://github.com/tefra/xsdata/pull/780))
- Added an option to set the encoding in the SOAP Client.
  ([#773](https://github.com/tefra/xsdata/pull/773))
- Added a CLI flag to show debug messages.
- Added a debug message for possible circular references during code generation.
- Added support to generate prohibited fields when they restrict parent fields.
  ([#781](https://github.com/tefra/xsdata/pull/781))

This release is bigger than intended and includes many major changes, that's why it took
so long.

## 22.12 (2022-12-17)

- Added option to ignore xml pattern restrictions
  [#727](https://github.com/tefra/xsdata/pull/727)
- Added globalns support via SerializerConfig
  [#724](https://github.com/tefra/xsdata/pull/724)
- Pinned docformatter version to v1.5.0 [#729](https://github.com/tefra/xsdata/pull/729)

## 22.11 (2022-11-06)

- Added list wrapper for elements and primitive nodes
  [#710](https://github.com/tefra/xsdata/pull/710)

## 22.9 (2022-09-24)

- Fixed code generation inconsistencies in different operating systems.
- Fixed circular imports error [#706](https://github.com/tefra/xsdata/pull/706)
- Fixed naming conflicts in imports [#706](https://github.com/tefra/xsdata/pull/706)
- Fixed issue with wrong occurrences in DTD code generation
  [#705](https://github.com/tefra/xsdata/pull/705)
- Fixed xs:group and xs:attrGroup name conflicts
  [#702](https://github.com/tefra/xsdata/pull/702)
- Added mathml3 in standard schemas

## 22.8 (2022-08-21)

- Added pycode serializer [#626](https://github.com/tefra/xsdata/issues/626)
- Added option to filter out unused global types
  [#691](https://github.com/tefra/xsdata/issues/691)
- Avoid using generics for mixed content when possible
  [#696](https://github.com/tefra/xsdata/pull/696)
- Removed support for python 3.6 [#671](https://github.com/tefra/xsdata/pull/671)

## 22.7 (2022-07-22)

- Fix empty lists do not get serialized
  [#686](https://github.com/tefra/xsdata/issues/686)
- Added external DTD code generator [#688](https://github.com/tefra/xsdata/pull/688)
- Added support for python 3.11

In the next release we will drop python 3.6 support!!!

## 22.5 (2022-05-08)

- Added support for xml date/time nanoseconds
  [#679](https://github.com/tefra/xsdata/pull/679)

## 22.4 (2022-04-10)

- Added config option to unnest classes
- Added new class meta option global_type, to hide classes from discovery
- Removed min/max length restrictions for enum type fields
- Allow builtin xml types to be fully extended
  [#672](https://github.com/tefra/xsdata/pull/672)

## 22.3 (2022-03-20)

- Added official support for python 3.11
- Fixed enumerations restricting complex types
  [#659](https://github.com/tefra/xsdata/issues/659)
- Fixed attribute name duplicate check to avoid invalid slugs

## 22.2 (2022-02-06)

- Fixed substitution groups on duplicate global types
  [#648](https://github.com/tefra/xsdata/issues/648)
- Added Postponed Annotations config option
  [#646](https://github.com/tefra/xsdata/issues/646)
- Added support for subclasses with different namespaces
  [#654](https://github.com/tefra/xsdata/issues/654)

## 22.1 (2022-01-23)

- Added recursive glob for cli dir source
  [#643](https://github.com/tefra/xsdata/issues/643)
- Added cfg options to change/force compound field names
  [#639](https://github.com/tefra/xsdata/issues/639)

## 21.12 (2021-12-05)

- Fixed wsdl generator to use operation name for rpc input messages
  [#609](https://github.com/tefra/xsdata/issues/609)
- Fixed wsdl generator to check for qualified elements for message part types
  [#612](https://github.com/tefra/xsdata/issues/612)
- Fixed compound field matcher to prefer exact types over derived
  [#617](https://github.com/tefra/xsdata/issues/617)
- Added async to the reserved keywords
  [#600](https://github.com/tefra/xsdata/issues/600)
- Added generator config for search & replace substitutions
  [#624](https://github.com/tefra/xsdata/issues/624)
- Updated code generator to remove abstract elements from class attrs
  [#627](https://github.com/tefra/xsdata/issues/627)
- Updated code generator to filter out all unused types
  [#629](https://github.com/tefra/xsdata/issues/629)

## 21.11 (2021-11-02)

- Fixed unescaped quotes in regex pattern
  [#592](https://github.com/tefra/xsdata/issues/592)
- Added config option fail_on_unknown_attributes
  [#597](https://github.com/tefra/xsdata/issues/597)
- Fixed build for python 3.10

## 21.9 (2021-09-04)

- Automate cli generate options [#578](https://github.com/tefra/xsdata/pull/578)
  - Generate cli options by the config model
  - Allow to enable/disable any flag
  - Allow to bypass any value from the config
  - Removed -cf/-ri as we can't have switches with short names

- Fixed generator not cascading default values to inner classes
  [#579](https://github.com/tefra/xsdata/issues/579)
- Re-raise xml syntax errors as xsdata.exceptions.ParserError
  [#571](https://github.com/tefra/xsdata/issues/571)
- Added cli summary with recovered warnings and issues
  [#583](https://github.com/tefra/xsdata/pull/583)
- Removed the native and lxml SAX handlers
  [#582](https://github.com/tefra/xsdata/issues/582)

## 21.8 (2021-08-03)

- Deprecated JsonSerializer indent property, use SerializerConfig instead
- Fixed SchemaMapper assigning wrong namespace for imported unqualified elements
- Fixed AttributeTypeHandler to maintain occurs between any flattening
- Fixed missing required field metadata property
- Fixed nillable fields not being marked as optional
- Fixed fields ordering during class reduce process (Codegen from xml/json)
- Added support for xs:defaultOpenContent:appliesToEmpty attribute
- Added ParserConfig class factory option
  [#549](https://github.com/tefra/xsdata/pull/549)
- Added SerializerConfig option to ignore optional default attributes
  [#555](https://github.com/tefra/xsdata/pull/555)
- Added warning on unexpected duplicate types
  [#564](https://github.com/tefra/xsdata/pull/564)
- Added GeneratorConfig support for kw_only and slots for python >= 3.10
- Added structure style namespace-clusters
  [#573](https://github.com/tefra/xsdata/pull/573)
- Updated text fields default value to empty string and marked as required
  [#570](https://github.com/tefra/xsdata/pull/570)
- Updated fields derived from xs:substitutionGroups to optional
- Updated fields derived from xs:any to optional
- Updated AttributeDefaultValueHandler to preserve acceptable default values
- Updated AttributeDefaultValueHandler to mark as optional any xsi:type attribute
- Updated xs:alternative handling to resemble xs:choice
- Updated mixed content handler to group all elements under wildcard
- Updated ElementMapper to detect nillable types
- Updated DictMapper to generate list of xs:anySimpleType for empty list nodes
- Updated the compatibility layer for dataclass style plugins
- Updated namespaces structure style to convert namespaces similar to jaxb
  - `http://www.w3.org/XML/1998/namespace` to `org.w3.XML.1998.namespace`

- Update binding process for nillable types and fields
  - nillable types can be initialized
  - nillable fields are initialized with None values

## 21.7 (2021-07-01)

- Fixed docstrings backslash escaping [#518](https://github.com/tefra/xsdata/pull/518)
- Fixed analyzer flattening bare types [#541](https://github.com/tefra/xsdata/pull/541)
- Fixed multiple issues with compound fields and override fields
  [#533](https://github.com/tefra/xsdata/pull/533)
- Fixed missing derived elements types during xml parsing
  [#541](https://github.com/tefra/xsdata/pull/541)
- Added structure style: clusters for smaller packages
  [#509](https://github.com/tefra/xsdata/pull/509)
- Added configuration to generate relative imports
  [#519](https://github.com/tefra/xsdata/pull/519)
- Added configuration to toggle all dataclasses features
  [#529](https://github.com/tefra/xsdata/pull/529)
- Added binding support for tuple typing annotations (frozen dataclasses)
  [#529](https://github.com/tefra/xsdata/pull/529)
- Added support to bind data directly from xml/lxml Element and ElementTree
  [#531](https://github.com/tefra/xsdata/pull/531)
  [#546](https://github.com/tefra/xsdata/pull/546)
- Updated analyzer to avoid same name for outer-inner classes
  [#511](https://github.com/tefra/xsdata/pull/511)
- Updated cli to fail early if config file is invalid
  [#514](https://github.com/tefra/xsdata/pull/514)
- Updated cli to remove setuptools from runtime dependencies
  [#515](https://github.com/tefra/xsdata/pull/515)
- Updated analyzer to relax override field validations completely
  [#516](https://github.com/tefra/xsdata/pull/516)
- Updated analyzer to sort classes before class name conflict resolution
  [#517](https://github.com/tefra/xsdata/pull/517)
- Updated JSON parser to attempt binding against subclasses
  [#527](https://github.com/tefra/xsdata/pull/527)
- Updated analyzer to guard against multiple substitution group runs
  [#538](https://github.com/tefra/xsdata/pull/538)
- Updated code generation to use case-sensitive reserved words
  [#545](https://github.com/tefra/xsdata/pull/545)

## 21.6 (2021-06-01)

- Fixed no args Dict annotation, raising an exception
  [#494](https://github.com/tefra/xsdata/issues/494)
- Fixed original name case not working for field names
  [#498](https://github.com/tefra/xsdata/issues/498)
- Fixed element type resolution with duplicate name conflicts
  [#503](https://github.com/tefra/xsdata/issues/503)
- Added handler to flatten bare inner classes
- Added the ability for custom types to subclass named tuples
- Added keyword meta in the reserved words
  [#491](https://github.com/tefra/xsdata/issues/491)
- Added new xml type `Ignore` to skip fields during binding
  [#504](https://github.com/tefra/xsdata/issues/504)
- Updated generic model DerivedElement.substituted flag with xsi:type
- Updated core components to improve binding performance
  - Converted almost all internal dataclasses to simple objects with **slots**
  - Converted the internal xml date/time types to named tuples
  - Reduced models metadata lookup times and memory footprint

- Updated JSON parser [#495](https://github.com/tefra/xsdata/issues/495)
  - Support failing on unknown properties
  - Support required properties
  - Support parser config
  - Stricter binding process
  - Enhance DerivedElement support

- Moved Definitive XML Schema tests to the samples repository

## 21.5 (2021-05-07)

- Added output structure style single-package
  [#469](https://github.com/tefra/xsdata/issues/469)
- Added support for marshalling array of objects for json
  [#448](https://github.com/tefra/xsdata/issues/448)
- Added support to generate code from raw json documents
  [#445](https://github.com/tefra/xsdata/issues/445)
- Added docstring style Blank to avoid generating them
  [#460](https://github.com/tefra/xsdata/issues/460)
- Added validations for non-supported type hints
- Added support for python 3.10
- Generate package **all** lists [#459](https://github.com/tefra/xsdata/issues/459)
- Generate factory for xs:list enumeration default values
  [#471](https://github.com/tefra/xsdata/issues/471)
- Avoid generating prohibited elements with maxOccurs==0
  [#478](https://github.com/tefra/xsdata/issues/478)
- Avoid generating identical overriding fields
  [#466](https://github.com/tefra/xsdata/issues/466)
- Fixed flattening base classes if they are also subclasses
  [#473](https://github.com/tefra/xsdata/issues/473)
- Fixed unchecked class name conflict resolution
  [#457](https://github.com/tefra/xsdata/issues/457)
- Refactored context components to improve binding performance
  [#476](https://github.com/tefra/xsdata/issues/476)

## 21.4 (2021-04-02)

- Split requirements to extras cli, soap and lxml
  [#419](https://github.com/tefra/xsdata/issues/419)
- Fixed parser conflict when an attribute and element field have the same qualified name
- Added cli auto-detection for source types, removed cli flag `--wsdl`
- Added cli support to generate code from raw xml documents
- Added cli entry point to allow pluggable output formats
  [#429](https://github.com/tefra/xsdata/issues/429)
- Added cli short flags for all options and flags
- Added handler to set effective choice groups
  [#433](https://github.com/tefra/xsdata/issues/433)
- Moved plantUML output format to a standalone
  [plugin](https://github.com/tefra/xsdata-plantuml)
- Updated xml parser to allow unions of primitive and class types
- Updated XmlDateTime parser to catch invalid cases with extra leading zeros
- Updated QName converter to validate uri/ncname when parsing string representations
- Updated JsonParser to allow parsing from filename string
- Updated cli option `--compound-fields` to a boolean flag

## 21.3 (2021-03-04)

- Added constant name convention config
  [#407](https://github.com/tefra/xsdata/issues/407)
- Added naming schemes screaming snake case and original case
- Updated xsi:lookup on xs:any derived elements
  [#315](https://github.com/tefra/xsdata/issues/315)
- Updated fields restriction inheritance
  [#417](https://github.com/tefra/xsdata/issues/417)
- Updated cli to allow package override from arguments
  [#416](https://github.com/tefra/xsdata/issues/416)
- Updated code generation to merge duplicate global types earlier
  [#406](https://github.com/tefra/xsdata/issues/406)
- Fixed docstrings issue breaking python syntax
  [#403](https://github.com/tefra/xsdata/issues/403)
- Fixed bindings for nillable content without workarounds
  [#408](https://github.com/tefra/xsdata/issues/408)
- Fixed resolver to apply aliases on extensions and choice fields
  [#414](https://github.com/tefra/xsdata/issues/414)
- Fixed schema models limiting xs:appinfo occurrences
  [#420](https://github.com/tefra/xsdata/issues/420)
- Decoupled core systems from click and lxml

**Notice**: In the next release installation profiles will be introduced that will turn
the cli, lxml and soap features **optional**.

## 21.2 (2021-02-02)

- Added class name context for user naming schemes
  [#348](https://github.com/tefra/xsdata/issues/348)
- Added mixed pascal naming scheme [#348](https://github.com/tefra/xsdata/issues/348)
- Added access to element/attribute name generators
  [#381](https://github.com/tefra/xsdata/issues/381)
- Added XmlHexBinary/XmlBase64Binary builtin data types
  [#387](https://github.com/tefra/xsdata/issues/387)
- Added support for xs:anyType root elements
  [#399](https://github.com/tefra/xsdata/issues/399)
- Updated JSON binding modules to use the fields local name
  [#389](https://github.com/tefra/xsdata/issues/389)
- Updated enum classes generation
  - Promote all inner enums to root [#383](https://github.com/tefra/xsdata/issues/383)
  - Fixed issues with producing invalid members
    [#385](https://github.com/tefra/xsdata/issues/385)
  - Added support for list/tuple member values
- Updated parsers accuracy for Union types
- Updated dependency resolution accuracy
- Update base classes generation strategies
- Updated builtin data types with helper constructors/methods
- Fixed inner class names conflicts [#375](https://github.com/tefra/xsdata/issues/375)
- Fixed issue not generating fields derived from xs:alternative elements
  [#393](https://github.com/tefra/xsdata/issues/393)
- Fixed duplicate root class name regression from v20.12
- Fixed issue adding unused lib imports
- Fixed issue adding unused name properties to choice elements

This is a sleeper release ✨✨✨ so many code generation improvements and finally the
JSON binding is aligned with XML.

## 21.1 (2021-01-08)

- Fixed XmlWriter converting attribute keys to QName.
  [#346](https://github.com/tefra/xsdata/issues/346)
- Set empty complexType base to anySimpleType
  [#349](https://github.com/tefra/xsdata/issues/349)
- Improve duplicate attr names detection
  [#351](https://github.com/tefra/xsdata/issues/351)
- Add SerializerConfig::xml_declaration option
  [#357](https://github.com/tefra/xsdata/issues/357)
- Generate default value/factory for compound fields
  [#359](https://github.com/tefra/xsdata/issues/359)
- Fixed default value for token fields
  [#360](https://github.com/tefra/xsdata/issues/360)
- Add doc metadata for compound fields
  [#362](https://github.com/tefra/xsdata/issues/362)
- JsonParser: handle class and primitive unions
  [#369](https://github.com/tefra/xsdata/issues/369)
- Update python mappings [#366](https://github.com/tefra/xsdata/issues/366)
  - Map xs:hexBinary and xs:base64Binary to bytes
  - Map xs:date/time types to builtin types XmlDate/Time
  - Map xs:duration to builtin type XmlDuration
  - Map xs:g[Year[Month[Day]]] to builtin type XmlPeriod
  - Map xs:Notation to QName
  - Add converter adapters for datetime.date/time
  - Add fields metadata key 'format' for time/date/binary types
  - Fixed issues with default literal values
  - Fixed issue with random field types order

## 20.12 (2020-12-10)

- Added SerializerConfig with new options.
  [#268](https://github.com/tefra/xsdata/issues/268),
  [#320](https://github.com/tefra/xsdata/issues/320)
- Added docstring styles: rst, google, numpy, accessible.
  [#318](https://github.com/tefra/xsdata/issues/318),
  [#340](https://github.com/tefra/xsdata/issues/340)
- Added `max line length` generator configuration.
  [#342](https://github.com/tefra/xsdata/issues/342)
- Added dynamic type locator for parsers.
  [#332](https://github.com/tefra/xsdata/issues/332)
- Fixed multiple issues with json binding.
  `98[7%](https://github.com/tefra/xsdata-w3c-tests/actions) successful roundtrips

## 20.11.1 (2020-11-13)

- Catch all type errors on xsi cache build
  [#316](https://github.com/tefra/xsdata/issues/316)

## 20.11 (2020-11-10)

- Added sub command to download remote schemas and definitions.
  [#279](https://github.com/tefra/xsdata/issues/279)
- Added new optional xml type `Elements` to maintain ordering for repeatable choices.
  [#296](https://github.com/tefra/xsdata/issues/296)
- Added xsi:type lookup procedure for xs:anyType derived elements.
  [#306](https://github.com/tefra/xsdata/issues/306)
- Updated simple type flattening detection.
  [#286](https://github.com/tefra/xsdata/issues/286)
- Updated generator to allow namespace structure on schemas without target namespace.
- Updated generator to avoid writing min/max occurs metadata for implied values.
  [#297](https://github.com/tefra/xsdata/issues/297)
- Update generator to use literal dictionary initialization.
- Updated parser security, disable lxml network and entities resolve.
- Fixed field types detection for elements with xs:alternative children.
  [#284](https://github.com/tefra/xsdata/issues/284)
- Fixed file generation to enforce default charset UTF-8.
  [#302](https://github.com/tefra/xsdata/issues/302)
- Fixed jinja2 undefined namespace var collision.
  [#298](https://github.com/tefra/xsdata/issues/298)
- Fixed import class name collision. [#300](https://github.com/tefra/xsdata/issues/300)
- Fixed restriction inheritance on xs:group elements.
  [#301](https://github.com/tefra/xsdata/issues/301)

## 20.10 (2020-10-02)

- Fixed generator adding multiple default value fields.
  [#249](https://github.com/tefra/xsdata/issues/249)
- Fixed generator not applying nested container restrictions.
  [#263](https://github.com/tefra/xsdata/issues/253)
- Fixed generator to avoid case insensitive class name conflicts.
  [#269](https://github.com/tefra/xsdata/issues/269)
- Fixed generator rendering unused simple types.
- Fixed generator unsorted libraries imports.
- Fixed JsonParser trying to parse init=False fields.
  [#253](https://github.com/tefra/xsdata/issues/253)
- Fixed NodeParser binding tail content more than once with mixed vars.
  [#256](https://github.com/tefra/xsdata/issues/256)
- Added XmlWriter interface to decouple serialize from lxml.
  [#247](https://github.com/tefra/xsdata/issues/247)
- Added native python xml content writer XmlEventWriter. ✨✨✨
- Added lxml based content writer LxmlEventWriter.
- Added generator config with options to control naming cases and aliases.
  [#265](https://github.com/tefra/xsdata/issues/265)
- Updated field xml type auto-detection to be more flexible.
  [#246](https://github.com/tefra/xsdata/issues/246)
- Updated EnumConverter to resort to canonical form matching as last resort.
  [#273](https://github.com/tefra/xsdata/issues/273)
- Updated support for derived elements.
  [#267](https://github.com/tefra/xsdata/issues/267)

This is my favorite release so far, maybe because xsdata reached one year of development
✨✨✨ or maybe because some of the last original components finally got the rewrite
they deserved.

## 20.9 (2020-09-03)

- Added field metadata key `tokens` for xs:list or xs:NMTOKENS derived elements.
- Added datatype factory to register custom converters.
- Added XmlHandler interface to decouple parsing from lxml.
- Added lxml based content handlers: LxmlEventHandler, LxmlSaxHandler
- Added native python xml content handlers: XmlEventHandler, XmlSaxHandler
- Added support for python >= 3.6 [#241](https://github.com/tefra/xsdata/issues/241)
- Added codegen for soap 1.1 fault messages.
- Fixed converting to enum members derived from xs:NMTOKENS.
- Fixed package level import naming conflicts.
  [#228](https://github.com/tefra/xsdata/issues/206)
- Fixed xml serializing to allow empty strings in attribute values.
  [#230](https://github.com/tefra/xsdata/issues/230)
- Fixed xml serializing for mixed content with non generics.
  [#238](https://github.com/tefra/xsdata/issues/238)

## 20.8 (2020-08-01)

- Added codegen support for **WSDL 1.1 and SOAP 1.1** bindings.
- Added experimental web services client.
- Added cli flag `--ns-struct` to group classes by target namespaces.
  [#206](https://github.com/tefra/xsdata/issues/206)
- Added parser config to support xinclude statements.
  [#207](https://github.com/tefra/xsdata/issues/207)
- Added new xml union node to improve bindings for fields with union type.
  [#207](https://github.com/tefra/xsdata/issues/207)
- Fixed class resolve issue with mixed namespaces.
  [#204](https://github.com/tefra/xsdata/issues/204)
- Fixed attribute comparison issue. [#209](https://github.com/tefra/xsdata/issues/209)
- Fixed data type mapping for various schema elements.
  [#221](https://github.com/tefra/xsdata/issues/221)
- Fixed mixed content handling. [#213](https://github.com/tefra/xsdata/issues/213)
- Code cleanup & 100% coverage.

## 20.7 (2020-07-04)

- Updated analyzer to allow abstract types to be generated.
  [#199](https://github.com/tefra/xsdata/issues/199)
- Removed support to generate code from multiple sources.
  [#172](https://github.com/tefra/xsdata/issues/172)
- Fixed naming conflict with AttributeGroup analyzer handler.
  [#194](https://github.com/tefra/xsdata/issues/194)
- Fixed analyzer to merge redefined attribute groups.
  [#196](https://github.com/tefra/xsdata/issues/196)
- Fixed analyzer to block inheritance on xs:override derived types.
  [#198](https://github.com/tefra/xsdata/issues/198)
- Refactored code to prepare for wsdl support.

## 20.6 (2020-06-01)

- Updated XmlSerializer to render default namespace whenever possible.
- Fixed issue generating modules outside the target package.
- Fixed issue not creating nested package **init** files.
- Code cleanup & docstrings

## 20.5.5 (2020-05-23)

- Added version option in the xsdata cli.
- Added generation of missing python **init** files.
- Added support for default values to inner enum classes.
- Fixed multiple issues with abstract classes and attributes/extension flattening.
- Fixed instance cross references causing codegen unpredictable results.
- Fixed xml serialization of wildcard attributes with user defined model values.
- Fixed issue with redefined/override elements with annotations.
- Fixed expand attribute groups recursively.
- Fixed false positive circular references.
- Fixed enumeration unions detection.
- Refactored ClassAnalyzer to smaller components.

## 20.5.4 (2020-05-15)

- Fix flattening enumeration unions.
- Fix generation for enum fields with default/fixed value.
- Fix duplicate attribute names handler to be case-insensitive.

## 20.5.1 (2020-05-14)

- Added support to fetch remote schemas.
- Updated duplicate attribute names handling.
- Updated code generation for enum type fields and default values.
- Fixed issue not generating classes derived from simple types.
- Fixed analyzer reaching the maximum recursion depth.
- Fixed analyzer to flatten properly inner self referencing classes.
- Moved dataclasses python conventions to jinja filters.

## 20.5 (2020-05-02)

- Updated codegen cli to accept multiple definitions or directories as argument.
- Update ClassBuilder to recursively search for anonymous types.
- Updated XmlParser to be thread-safe.
- Added performance tweaks on XmlParser.
- Added parser config to fail or not on unknown properties.
- Fixed primitive types being marked as forward references.
- Fixed nested restrictions on xs:simpleType.
- Fixed ClassAnalyzer to recover/ignore missing types.

## 20.4.2 (2020-04-21)

- Added support for abstract xsi:types in XmlParser.
- Added cache for event names in XmlParser.
- Added sanitization for generated module names.
- Fixed not flattening abstract extension.
- Fixed extension name conflicts between simple and complex types.
- Fixed possible memory leak in CodeWriter.
- Fixed looping variables twice to find next node in XmlParser.
- Fixed CodeWriter adding unnecessary new lines.

## 20.4.1 (2020-04-13)

- Fixed open content attribute with mode suffix to be generated last.
- Fixed issues with wildcard and mixed content parsing.
- Updated xs:qname mapping to lxml.QName
- Updated support for xs:list.
- Updated parser to ignore xsi:type attributes default/fixed values.
- Refactored code components.
- Pass more than 99% of the `W3C XML Schema 1.1 test cases
  https://travis-ci.org/tefra/xsdata-w3c-tests

## 20.4 (2020-04-01)

- Added support for sequential fields.
- Added support for open content.
- Added support multiple redefined elements.
- Updated support for wildcards to be aware of generic namespaces.
- Updated support for wildcards to be aware of non-generic objects.
- Updated codegen to run after fully parsing all the definitions.
- Updated codegen to skip unresolved schema locations.
- Updated xml parser to ignore comments.
- Updated xml parser to retain a copy of the input namespaces.
- Fixed issues with nillable fields being ignored.
- Fixed multiple issues with wrong restrictions being applied.
- Fixed binding issues when there are naming conflicts.
- Fixed serialization for inf/nan/exponential float and decimal values.
- Fixed naming conflicts with class/package names.
- Fixed multiple circular import issues during parsing and code generation.
- Pass more than 98% of the `W3C XML Schema 1.1 test cases
  https://travis-ci.org/tefra/xsdata-w3c-tests

## 20.3 (2020-03-01)

- Added copies of common schemas xlink, xsi, xml.
- Added XML Schema 1.1 models and properties.
- Added support for redefines, overrides, alternatives and default attributes.
- Added missing xsd data types: dateTimestamp, anyType, anyAtomicType.
- Added protection against duplicate class fields enumerations.
- Added python common types to the stop word list.
- Updated wildcards parsing to avoid duplicate elements.
- Updated native datatype detection made stricter.
- Updated enumerations generation to sort and filter values.
- Updated mapping xs:decimal to python Decimal
- Fixed elements/attribute not inheriting namespaces from references.
- Fixed module names collisions.
- Fixed self referencing classes.
- Fixed class name collisions complexTypes vs elements.
- Fixed parsers not respecting default values.
- Fixed AbstractXmlParser to handle leafless root nodes.
- Pass more than 90% of the `W3C XML Schema 1.1 test cases
  https://travis-ci.org/tefra/xsdata-w3c-tests.

## 20.2 (2020-02-09)

- Added support xs:any and xs:anyAttribute elements.
- Added support for auto-detecting XML Schema namespace prefix.
- Added support for xml datatypes lang and base.
- Refactored SchemaParser to use the XmlParser.
- Updated XmlParser to bind after elements are fully parsed.

## 20.1.3 (2020-01-26)

- Fixed elements min|man occurs inheritance from their container.
- Fixed global elements and attributes are now always qualified.
- Fixed including no namespace schemas.
- Fixed list elements attribute handling.
- Added support for unqualified elements.
- Added support for qualified attributes.
- Added support for nillable elements.
- Added support for unions of member and simple types.
- Added binding test suite

## 20.1.2 (2020-01-13)

- Generate anonymous Enumerations
- Generate attributes from List and Union elements
- Fix restriction inheritance
- Officially support python 3.8
- Completely migrate to setup.cfg
- Introduce integration test suite

## 20.1.1 (2020-01-09)

- Change print mode to print rendered output
- Added new format PlantUML class diagram to replace the old print/debug mode

## 20.1 (2020-01-07)

- Initial release
</details>
