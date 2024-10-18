# 머신러닝을 통한 급발진 사고 학습 및 예방


## 개발 동기

최근 급 발진 사고가 많아 피해를 보는 사례가 많아지고 있다. 급 발진 사고는 크게 사용자 과실과 자동차 결함으로 인한 원인으로 구분 되지만, 머신 러닝을 통해 두 가지의 사례를 구별하여 각각의 대처 방안을 통해 사고를 예방 할 것이다


## 구현방법

1. **데이터 수집** : 사용자 운전습관이나 다른 운전자의 운전 데이터를 수집
2. **데이터 전처리** : 값이 평균에 많이 벗어나거나 이상한 데이터를 삭제하거나 중요한 데이터를 전처리
3. **실시간 데이터 처리** : 서버를 통해 실시간으로 차량과 데이터 공유
4. **머신러닝 모델 학습 & 사고 예방 처리** : 머신러닝 모델 구현 후, 학습시켜 사고가 일어났을 시 운전자에게 경고 혹은 직접 차체 제어
5. **피드백** : 모델 구현 후, 더 나은 결과를 위해 모델 업데이트 혹은 수정


## LSTM 모델 예시 코드(ChatGPT) - python

    import numpy as np

    class LSTM:
    def __init__(self, input_size, hidden_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        
        # Weight matrices for input, forget, output gates and cell state
        self.Wf = np.random.randn(hidden_size, input_size + hidden_size)
        self.Wi = np.random.randn(hidden_size, input_size + hidden_size)
        self.Wo = np.random.randn(hidden_size, input_size + hidden_size)
        self.Wc = np.random.randn(hidden_size, input_size + hidden_size)
        
        # Bias terms
        self.bf = np.zeros((hidden_size, 1))
        self.bi = np.zeros((hidden_size, 1))
        self.bo = np.zeros((hidden_size, 1))
        self.bc = np.zeros((hidden_size, 1))

        # Cell state and hidden state initialization
        self.h_prev = np.zeros((hidden_size, 1))
        self.c_prev = np.zeros((hidden_size, 1))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def tanh(self, x):
        return np.tanh(x)

    def forward(self, x):
        # Combine input and previous hidden state
        concat = np.concatenate((self.h_prev, x), axis=0)

        # Forget gate
        ft = self.sigmoid(np.dot(self.Wf, concat) + self.bf)

        # Input gate
        it = self.sigmoid(np.dot(self.Wi, concat) + self.bi)
        c_tilde = self.tanh(np.dot(self.Wc, concat) + self.bc)

        # Update cell state
        self.c_prev = ft * self.c_prev + it * c_tilde

        # Output gate
        ot = self.sigmoid(np.dot(self.Wo, concat) + self.bo)

        # Update hidden state
        self.h_prev = ot * self.tanh(self.c_prev)

        return self.h_prev

    # Example usage:
    input_size = 10  # Number of input features
    hidden_size = 20  # Number of hidden units

    lstm = LSTM(input_size, hidden_size)

    # Sample input (random example)
    x = np.random.randn(input_size, 1)
    output = lstm.forward(x)

    print("LSTM Output:", output)


##예상 결과

여러 가지 상황의 운전 데이터를 확보할 수 있으며, 이를 통해 머신러닝 모델을 학습시켜 사고 상황 발생시 적절한 대처를 할 수 있을 것이다. 


## 출처

[최근 급발진으로 인한 교통사고 현황] (https://taas.koroad.or.kr/)<https://taas.koroad.or.kr>

[LSTM 모델 기본 개념] (https://ctkim.tistory.com/entry/LSTMLong-short-time-memory-%EA%B8%B0%EC%B4%88-%EC%9D%B4%ED%95%B4)<https://ctkim.tistory.com/entry/LSTMLong-short-time-memory-%EA%B8%B0%EC%B4%88-%EC%9D%B4%ED%95%B4>
