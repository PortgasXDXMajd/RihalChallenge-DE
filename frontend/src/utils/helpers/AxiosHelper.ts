import axiosMain from 'axios';
import { toast } from 'sonner';
import { BASE_HTTPS } from '../environment_var';

const axios = axiosMain.create({
  baseURL: BASE_HTTPS,
});

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    const response = error.response;

    if (response) {
      switch (response.status) {
        case 400:
          toast.error(
            response.data?.message || 'Bad request. Please check your input.'
          );
          break;

        case 404:
          toast.info(response.data?.message || 'Resource not found.');
          break;

        default:
          toast.error(
            response.data?.message || 'An unexpected error occurred.'
          );
          break;
      }
    } else {
      toast.error('Network error. Please check your connection.');
    }

    return Promise.resolve({
      data: null,
      status: response?.status || 500,
      error: response?.data?.message || 'Error occurred',
    });
  }
);

export { axios };
