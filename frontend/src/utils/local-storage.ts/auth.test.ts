import { setAccessToken, getAccessToken, setTokenType, getTokenType } from './auth';
import { LocalStorageKey } from '../../data/enums';

describe('setAccessToken and getAccessToken', () => {
    beforeEach(() => {
        let token : string | null = "";
        Storage.prototype.setItem = jest.fn().mockImplementation((_, value: string) => {
            token=value;
        });
        
        Storage.prototype.getItem = jest.fn().mockImplementation(() => {return token});
        Storage.prototype.removeItem = jest.fn().mockImplementation(() => {
            token = null;
        });
    });
  
    it('should set and get the access token correctly', () => {    
        // Act
        setAccessToken("abc");
        const result = getAccessToken();
    
        // Assert
        expect(localStorage.setItem).toHaveBeenCalledWith(LocalStorageKey.ACCESS_TOKEN, "abc");
        expect(result).toEqual("abc");
    });

    it('should remove the access token from local storage if null is passed to setAccessToken', () => {
        // Arrange
        const accessToken = 'abc';
        setAccessToken(accessToken);
    
        // Act
        setAccessToken(null);
        const result = getAccessToken();
    
        // Assert
        expect(localStorage.removeItem).toHaveBeenCalledWith(LocalStorageKey.ACCESS_TOKEN);
        expect(result).toBeNull();
    });
});

describe('setTokenType and getTokenType', () => {
    beforeEach(() => {
        let token : string | null = "";
        Storage.prototype.setItem = jest.fn().mockImplementation((_, value: string) => {
            token=value;
        });
        
        Storage.prototype.getItem = jest.fn().mockImplementation(() => {return token});
        Storage.prototype.removeItem = jest.fn().mockImplementation(() => {
            token = null;
        });
    });
  
    it('should set and get the token type correctly', () => {
      // Arrange
      const tokenType = 'Bearer';
  
      // Act
      setTokenType(tokenType);
      const result = getTokenType();
  
      // Assert
      expect(localStorage.setItem).toHaveBeenCalledWith(LocalStorageKey.TOKEN_TYPE, tokenType);
      expect(result).toEqual(tokenType);
    });
  
    it('should remove the token type from local storage if null is passed to setTokenType', () => {
      // Arrange
      const tokenType = 'Bearer';
      setTokenType(tokenType);
  
      // Act
      setTokenType(null);
      const result = getTokenType();
  
      // Assert
      expect(localStorage.removeItem).toHaveBeenCalledWith(LocalStorageKey.TOKEN_TYPE);
      expect(result).toBeNull();
    });
});
