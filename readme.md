<!-- README.md for AD Project -->

<p align="center">
  <img src="https://img.shields.io/badge/Django-4.2-green" alt="Django">
  <img src="https://img.shields.io/badge/Python-3.11+-blue" alt="Python">


# AD 프로젝트 (웹 서버 컴퓨팅 과제)

> Django 기반 커뮤니티 웹 애플리케이션으로, "점프 투 장고(Jump to Django)" pybo(3–12장)을 확장하여 개발되었습니다.

---

## 📑 목차

- [팀 구성](#-팀-구성)
- [프로젝트 주요 기능](#-프로젝트-주요-기능)
  - [신규 서비스](#1-신규-서비스)
  - [교과서 서비스](#2-교과서-서비스)
- [설치 및 실행 방법](#-설치-및-실행-방법)
- [디렉토리 구조](#-디렉토리-구조)
- [문서 및 데모](#-문서-및-데모)
- [연락처](#✉️-연락처)
- [라이선스](#-라이선스)

---

## 📋 팀 구성

| 멤버 | 역할 | GitHub |
|:----:|:----:|:-----:|
| **이강욱** | Front-end, 백엔드 주요 로직, 배포 관리 | [@powerslam](https://github.com/powerslam) |
| **박재영** | DB 설계, API 연동, 테마 구현 | [@co2ma](https://github.com/co2ma) |

- **프로젝트 기간**: 2025.06

---

## 🚀 프로젝트 주요 기능

### 1. 신규 서비스

| 기능 | 설명 | 구현 방식 |
|:----|:-----|:---------|
| **북마크** | 관심 게시물을 즐겨찾기 | `Bookmark` 모델 (M:N), UI 토글 버튼 |
| **마이페이지 수정** | 프로필 정보(닉네임, 이메일, 이미지) 수정 | `Profile` 모델, `UpdateView`, `ModelForm` |
| **내 글 보기** | 내가 작성한 게시물 목록 조회 | `ListView` & `pagination` |
| **사용자 차단** | 특정 사용자 게시글/댓글 숨김 | `Block` 모델, 뷰/템플릿 레벨 필터링 |
| **라이트/다크 모드** | 사이트 테마 토글 | JS + `localStorage`, CSS 클래스 토글 |

### 2. 교과서 서비스

- **Markdown 렌더링**: `markdown2` 라이브러리 사용, 서버 사이드 변환  
- **검색 & 정렬**: `Q` 객체 + `order_by()`, 키워드 검색 및 최신·추천·조회수 정렬

---

## ⚙️ 설치 및 실행 방법

1. **레포지토리 클론**
   ```bash
   git clone https://github.com/your-org/AD_Project_wigo.git
   cd AD_Project_wigo/source_code
   ```
2. **가상 환경 생성 & 활성화**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. **패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```
4. **DB 마이그레이션**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **슈퍼유저 생성**
   ```bash
   python manage.py createsuperuser
   ```
6. **개발 서버 실행**
   ```bash
   python manage.py runserver
   ```
7. **접속**: `http://127.0.0.1:8000/`

---

## 📂 디렉토리 구조

```plaintext
AD_Project_wigo/
├── source_code/          # Django 프로젝트 전체
│   ├── accounts/         # 인증 및 프로필
│   ├── posts/            # 게시물 CRUD
│   ├── bookmarks/        # 북마크 앱
│   ├── blocks/           # 차단 앱
│   ├── templates/        # 공용 템플릿
│   ├── static/           # CSS, JS, 이미지
│   ├── AD_Project/       # 설정 디렉토리
│   └── manage.py         # 관리 커맨드
├── report/               # 보고서 (.docx, .pdf)
├── video/                # 시연 영상 (.mp4)
├── presentation/         # 발표 자료 (.pptx)
└── README.md             # 프로젝트 개요 및 안내
```

---

## 📄 문서 및 데모


- **시연 영상**: https://youtu.be/NpyeNl6Cg8s



---



## 📝 라이선스

이 프로젝트는 [MIT 라이선스](https://opensource.org/licenses/MIT) 하에 배포됩니다.

---

<p align="center">
  Made by 이강욱 & 박재영
</p>
