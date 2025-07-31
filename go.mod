module coderoot-bot

go 1.21

require (
	github.com/go-telegram-bot-api/telegram-bot-api/v5 v5.5.1
	go.mongodb.org/mongo-driver v1.12.1
	github.com/redis/go-redis/v9 v9.3.0
	github.com/joho/godotenv v1.5.1
	github.com/gin-gonic/gin v1.9.1
	go.uber.org/zap v1.25.0
	github.com/google/uuid v1.4.0
	github.com/prometheus/client_golang v1.17.0
	github.com/shirou/gopsutil/v3 v3.23.12
	github.com/gorilla/mux v1.8.1
	github.com/gorilla/handlers v1.5.2
	github.com/gorilla/websocket v1.5.1
	github.com/rs/cors v1.10.1
	github.com/urfave/negroni v1.0.0
	github.com/gorilla/securecookie v1.1.2
	github.com/gorilla/sessions v1.2.2
	github.com/golang-jwt/jwt/v5 v5.2.0
	github.com/golang-migrate/migrate/v4 v4.16.2
	github.com/lib/pq v1.10.9
	github.com/go-sql-driver/mysql v1.7.1
	github.com/mattn/go-sqlite3 v1.14.17
	github.com/jinzhu/gorm v1.9.16
	github.com/jinzhu/now v1.1.5
	github.com/aws/aws-sdk-go v1.48.16
	github.com/aliyun/aliyun-oss-go-sdk v2.2.9+incompatible
	github.com/tencentyun/cos-go-sdk-v5 v0.7.42
	github.com/minio/minio-go/v7 v7.0.66
	github.com/streadway/amqp v1.1.0
	github.com/nsqio/go-nsq v1.1.0
	github.com/segmentio/kafka-go v0.4.47
	github.com/elastic/go-elasticsearch/v8 v8.11.1
	github.com/olivere/elastic/v7 v7.0.32
	github.com/go-redis/redis/v8 v8.11.5
	github.com/go-redis/redis_rate/v10 v10.0.1
	github.com/patrickmn/go-cache v2.1.0+incompatible
	github.com/coocood/freecache v1.2.4
	github.com/valyala/fasthttp v1.50.0
	github.com/gofiber/fiber/v2 v2.50.0
	github.com/labstack/echo/v4 v4.11.3
	github.com/gin-contrib/cors v1.4.0
	github.com/gin-contrib/logger v0.2.6
	github.com/gin-contrib/requestid v0.0.6
	github.com/gin-contrib/sessions v0.0.5
	github.com/gin-contrib/static v0.0.1
	github.com/gin-contrib/timeout v0.0.3
	github.com/gin-contrib/pprof v1.4.0
	github.com/gin-contrib/gzip v0.0.6
	github.com/gin-contrib/secure v0.0.1
	github.com/gin-contrib/expvar v0.0.1
	github.com/gin-contrib/location v0.0.2
	github.com/gin-contrib/opengintracing v1.0.2
	github.com/gin-contrib/sse v0.1.0
	github.com/gin-contrib/zap v0.1.0
	github.com/gin-contrib/websocket v0.0.5
)

require (
	github.com/andybalholm/brotli v1.0.5 // indirect
	github.com/beorn7/perks v1.0.1 // indirect
	github.com/bytedance/sonic v1.9.1 // indirect
	github.com/cespare/xxhash/v2 v2.2.0 // indirect
	github.com/chenzhuoyu/base64x v0.0.0-20221115062448-fe3a3abad311 // indirect
	github.com/cloudflare/backoff v0.0.0-20161212185259-647f3cdfc87a // indirect
	github.com/davecgh/go-spew v1.1.2-0.20180830191138-d8f796af33cc // indirect
	github.com/dgryski/go-rendezvous v0.0.0-20200823014737-9f7001d12a5f // indirect
	github.com/felixge/httpsnoop v1.0.3 // indirect
	github.com/gabriel-vasile/mimetype v1.4.2 // indirect
	github.com/gin-contrib/sessions v0.0.5 // indirect
	github.com/gin-contrib/static v0.0.1 // indirect
	github.com/gin-contrib/timeout v0.0.3 // indirect
	github.com/gin-contrib/pprof v1.4.0 // indirect
	github.com/gin-contrib/gzip v0.0.6 // indirect
	github.com/gin-contrib/secure v0.0.1 // indirect
	github.com/gin-contrib/expvar v0.0.1 // indirect
	github.com/gin-contrib/location v0.0.2 // indirect
	github.com/gin-contrib/opengintracing v1.0.2 // indirect
	github.com/gin-contrib/sse v0.1.0 // indirect
	github.com/gin-contrib/zap v0.1.0 // indirect
	github.com/gin-contrib/websocket v0.0.5 // indirect
	github.com/go-ole/go-ole v1.2.6 // indirect
	github.com/go-playground/locales v0.14.1 // indirect
	github.com/go-playground/universal-translator v0.18.1 // indirect
	github.com/go-playground/validator/v10 v10.14.0 // indirect
	github.com/goccy/go-json v0.10.2 // indirect
	github.com/golang-jwt/jwt/v5 v5.2.0 // indirect
	github.com/google/uuid v1.4.0 // indirect
	github.com/gorilla/context v1.1.1 // indirect
	github.com/gorilla/securecookie v1.1.2 // indirect
	github.com/gorilla/sessions v1.2.2 // indirect
	github.com/gorilla/websocket v1.5.1 // indirect
	github.com/hashicorp/errwrap v1.1.0 // indirect
	github.com/hashicorp/go-multierror v1.1.1 // indirect
	github.com/inconshreveable/mousetrap v1.1.0 // indirect
	github.com/jinzhu/inflection v1.0.0 // indirect
	github.com/json-iterator/go v1.1.12 // indirect
	github.com/klauspost/compress v1.17.0 // indirect
	github.com/klauspost/cpuid/v2 v2.2.4 // indirect
	github.com/labstack/gommon v0.4.0 // indirect
	github.com/leodido/go-urn v1.2.4 // indirect
	github.com/lufia/plan9stats v0.0.0-20211012122336-39d0f177ccd0 // indirect
	github.com/mattn/go-colorable v0.1.13 // indirect
	github.com/mattn/go-isatty v0.0.19 // indirect
	github.com/mattn/go-runewidth v0.0.15 // indirect
	github.com/matttproud/golang_protobuf_extensions v1.0.4 // indirect
	github.com/modern-go/concurrent v0.0.0-20180306012644-bacd9c7ef1dd // indirect
	github.com/modern-go/reflect2 v1.0.2 // indirect
	github.com/pelletier/go-toml/v2 v2.0.8 // indirect
	github.com/pmezard/go-difflib v1.0.1-0.20181226105442-5d4384ee4fb2 // indirect
	github.com/power-devops/perfstat v0.0.0-20210106213030-5aafc221ea8c // indirect
	github.com/prometheus/client_model v0.4.1-0.20230718164431-9a2bf3000d16 // indirect
	github.com/prometheus/common v0.44.0 // indirect
	github.com/prometheus/procfs v0.11.1 // indirect
	github.com/rivo/uniseg v0.2.0 // indirect
	github.com/shoenig/go-m1cpu v0.1.6 // indirect
	github.com/spf13/pflag v1.0.5 // indirect
	github.com/tklauser/go-sysconf v0.3.12 // indirect
	github.com/tklauser/numcpus v0.6.1 // indirect
	github.com/twitchyliquid64/golang-asm v0.15.1 // indirect
	github.com/ugorji/go/codec v1.2.11 // indirect
	github.com/valyala/bytebufferpool v1.0.0 // indirect
	github.com/valyala/fasttemplate v1.2.2 // indirect
	github.com/xo/terminfo v0.0.0-20210125001918-ca9a967f8778 // indirect
	github.com/yusufpapurcu/wmi v1.2.3 // indirect
	golang.org/x/arch v0.3.0 // indirect
	golang.org/x/crypto v0.14.0 // indirect
	golang.org/x/net v0.17.0 // indirect
	golang.org/x/sys v0.13.0 // indirect
	golang.org/x/text v0.13.0 // indirect
	golang.org/x/term v0.13.0 // indirect
	golang.org/x/time v0.3.0 // indirect
	google.golang.org/protobuf v1.30.0 // indirect
	gopkg.in/yaml.v3 v3.0.1 // indirect
)

