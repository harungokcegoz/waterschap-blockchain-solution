#!/bin/bash

cd client

npm install
npm run docker:start:testnet
npm run dev
