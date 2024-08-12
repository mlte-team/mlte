// types/runtime-config.d.ts
declare module 'nuxt/schema' {
    interface RuntimeConfig {
      private: {
        apiKey: string;
      };
      public: {
        apiPath: string;
        version: string;
      };
    }
  }
  