import express from 'express';

export function createApp() {
  const app = express();
  app.disable('x-powered-by');
  app.get('/health', (_req, res) => {
    res.status(200).json({ status: 'ok', service: 'respawn-api', version: '0.1.0' });
  });
  app.use((_req, res) => {
    res.status(404).json({ error: 'not_found' });
  });
  return app;
}
