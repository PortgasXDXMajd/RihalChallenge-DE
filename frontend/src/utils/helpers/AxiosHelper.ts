import axiosMain from 'axios';
import { BASE_HTTPS } from '../environment_var';

const axios = axiosMain.create({
  baseURL: BASE_HTTPS,
});

export { axios };
