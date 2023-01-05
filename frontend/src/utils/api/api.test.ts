import axios from "axios"
import { assert } from "console";
import { getAccessToken, getTokenType} from "../local-storage.ts/auth"

import { axiosInstance, getHeaders } from "./api"

jest.mock("axios", () => {
    return {
        create: jest.fn().mockReturnValue({
            defaults: {
                baseURL: "",
            }
        })
    }
});

jest.mock('../local-storage.ts/auth', () => {
    return {
        getAccessToken: jest.fn().mockReturnValue("abc123"),
        getTokenType: jest.fn().mockReturnValue("bearer"),
    }
});

describe('getHeaders', () => {
    it('get the correct headers', () => {
        const config = getHeaders();
        expect(config).toEqual({
            headers: {
                "Authorization": "bearer abc123"
            }
        });
    });
});

describe('axiosInstance', () => {
    it('set the baseURL', () => {
        expect(axiosInstance.defaults.baseURL).toEqual("http://localhost:8000");
    });
})