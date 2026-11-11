import { createApp } from './app.js';
import { readConfig } from './config.js';

const { host, port } = readConfig();
const server = createApp().listen(port, host, () => {
  console.log(`Respawn API: http://${host}:${port}/health`);
});
for (const signal of ['SIGINT', 'SIGTERM']) {
  process.on(signal, () => server.close(() => process.exit(0)));
}
